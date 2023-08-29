import os
import shutil
import subprocess
import threading

import bpy

from .. import lod_num
from . import path as ph
from . import pbr, qc, smd, util, vmt, vtf

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def deploy_mat():
    
    source_folder = os.path.join(ph.work_folder(), "materials")
    destination_folder = os.path.join(ph.source(), "materials")
    
    shutil.copytree(source_folder, destination_folder)


def export_mesh():
    
    scene = bpy.context.scene
    smd.func_export_ref(lod_num, scene.ref_collection)
    
    scene = bpy.context.scene
    smd.func_export_pys(scene.pys_collection)
    
    qc.write_qc()
    qc.write_idle()
    
    util.run_exe()

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def export(scene):
    
    threads = []
    
    for material in get_materials():
        
        #work_folder = os.path.join(work_folder, str(material.name) )
        
        work_folder = os.path.join( ph.work_folder(), ph.path_material(), material.name)
        
        os.makedirs(work_folder, exist_ok=True)
        
        if scene.multithreading:
            thread = threading.Thread(target=process_material, args=(scene, material, work_folder))
            threads.append(thread)
            thread.start()
        else:
            process_material(scene, material, work_folder)
    
    if scene.multithreading:
        for thread in threads:
            thread.join()
    
    if scene.auto_deploy:
        deploy_mat()
    
    print("Export Done")

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def run_exe():
    
    cmd = f'"{ph.studiomdl()}" -game "{ph.source()}" -nop4 -verbose "compile.qc"'
    
    working_directory = os.path.join(ph.work_folder(), ph.path_compile_model())
    
    print(cmd)
    print(working_directory)
    
    subprocess.run(cmd, shell=True, cwd=working_directory)

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def process_material(scene, material, work_folder):
    
    nodes, status = decode_material_nodes(scene, material)
    
    if not scene.only_vmt:
        pbr.main(scene, nodes, status, material)
        if scene.convert_vtf:
            vtf.main(scene, work_folder)
    if scene.make_vmt or scene.only_vmt:
        vmt.main(scene, status, material.name)

def get_materials():
    active_materials = []
    
    for obj in bpy.context.scene.objects:
        for slot in obj.material_slots:
            if slot.material:
                active_materials.append(slot.material)
                
    return active_materials



def decode_material_nodes(scene, material):
    label_to_node_type = {
        scene.color_node_label: 'Color',
        scene.pbr_node_label: 'PBR',
        scene.normal_node_label: 'Normal',
        scene.light_node_label: 'Light'
    }

    nodes = {}
    for node in material.node_tree.nodes:
        if node.type == 'TEX_IMAGE' and node and node.label in label_to_node_type:
            nodes[label_to_node_type[node.label]] = node
    
    status = [label in nodes for label in label_to_node_type.values()]
    nodes_return = nodes.get('Color'), nodes.get('PBR'), nodes.get('Normal'), nodes.get('Light')
    
    if nodes.get('Color') or nodes.get('Normal'):
        return nodes_return, status
    else:
        return decode_nodes_fallback(scene, material)

def decode_nodes_fallback(scene, material):
    
    status_backup = [False, False, False, False]
    #has_color, has_pbr, has_normal, has_light
    
    nodes = {}
    
    # Try to get any tex_image connected to the base Color input of the BSDF shader, save it as Color
    bsdf_shader = None
    for node in material.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            bsdf_shader = node
            break
    if bsdf_shader:
        color_input = bsdf_shader.inputs.get('Base Color')
        if color_input and color_input.is_linked:
            linked_node = color_input.links[0].from_node
            if linked_node.type == 'TEX_IMAGE':
                nodes['Color'] = linked_node
                status_backup[0] = True
    
    # Do the same for the Normal and Emission nodes (if available)
    normal_input = bsdf_shader.inputs.get('Normal')
    if normal_input and normal_input.is_linked:
        linked_node = normal_input.links[0].from_node
        if linked_node.type == 'TEX_IMAGE':
            nodes['Normal'] = linked_node
            status_backup[2] = True
    
    emission_input = bsdf_shader.inputs.get('Emission')
    if emission_input and emission_input.is_linked:
        linked_node = emission_input.links[0].from_node
        if linked_node.type == 'TEX_IMAGE':
            nodes['Emission'] = linked_node
            status_backup[3] = True
    
    nodes_return_backup = (
        nodes.get('Color'),
        None,
        nodes.get('Normal'),
        nodes.get('Light')
    )
    
    return nodes_return_backup, status_backup

