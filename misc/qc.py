import logging as log
import os

import bpy

from .. import lod_num
from ..GUI import common
from . import path as ph
from . import util


def build():
    write_qc()
    write_idle()

def write_qc():
    scene = bpy.context.scene
    
    export_format = str.lower(scene.gbr_export_format)
    
    reference = "Reference"
    
    qc_path = os.path.join( ph.work_folder(), ph.path_compile_model())
    os.makedirs(qc_path, exist_ok=True)
    
    temp = os.path.join(qc_path, "compile.qc")
    
    with open( temp , 'w') as f:
        f.write('//Blender Source Addon\n')
        f.write('//Created By Glad_BR\n')
        f.write('\n')
        #Body
        if scene.staticprop:
            f.write('$staticprop\n')
            f.write('\n')
        
        f.write(f'$modelname "{ph.absolute_mdl()}"\n')
        
        f.write('\n')
        f.write('$bodygroup "Body"\n')
        f.write('{\n')
        f.write(f'\tstudio "{reference}.{export_format}"\n')
        f.write('}\n')
        f.write('\n')
        
        write_lod(f, scene, reference, export_format)
        
        f.write(f'$surfaceprop "{scene.surfaceprop}"\n')
        f.write('\n')
        f.write(f'$contents "{scene.contents}"\n')
        f.write('\n')
        f.write(f'$cdmaterials "{ph.material()}"\n')
        f.write('\n')
        
        if scene.make_skin_groups: write_texturegroup(f)
        
        f.write('\n')
        
        f.write(f'$collisionmodel "PYS.{export_format}"\n')
        f.write('{\n')
        if scene.concave:
            f.write(f'\t$concave\n')
        
        f.write(f'\t$mass {str(scene.mass)}\n')
        f.write(f'\t$inertia {str(scene.inertia)}\n')
        
        f.write(f'\t$maxconvexpieces 10000\n')
        f.write('}\n')
        f.write('\n')
        
        f.write(f'$sequence "idle" "{os.path.join("anims","idle.SMD")}"\n')
        f.write('\n')

def write_lod(f, scene, reference, export_format):
    if scene.make_lods:
        for [lod, ang] in lod_num:
            f.write(f'$lod {lod}\n')
            f.write('{\n')
            f.write(f'\treplacemodel "{reference}.{export_format}" "LOD_{lod}.{export_format}"\n')
            f.write(f'\tnofacial\n')
            f.write('}\n')
            f.write('\n')


def write_texturegroup(f):
    
    suffix = '_OFF'
    
    mats = util.get_materials()
    
    skin0 = ''
    skin1 = ''
    
    for mat in mats:
        if util.mat_has_light(mat):
            skin0 = skin0 + f'"{mat.name}" '
            skin1 = skin1 + f'"{mat.name + suffix}" '
    
    skin0 = '{ '+skin0+'}'
    skin1 = '{ '+skin1+'}'
    
    f.write(f'$texturegroup "skinfamilies"\n')
    f.write('{\n')
    f.write(f'\t{skin0}\n')
    f.write(f'\t{skin1}\n')
    f.write('}\n')
    
    print("")
    print(skin0)
    print(skin1)
    print("")



def write_idle():
    qc_path = os.path.join( ph.work_folder(), ph.path_compile_model(), "anims")
    os.makedirs(qc_path, exist_ok=True)
    
    File = [
        'version 1',
        'nodes',
        '0 "Implicit" -1',
        'end',
        'skeleton',
        'time 0',
        '0  0.000000 0.000000 0.000000  0.000000 0.000000 0.000000',
        'end',
        'triangles',
        'end'
    ]
    
    with open( str(os.path.join(qc_path, "idle.SMD")), 'w') as f:
        for string in File:
            f.write(f'{string}\n')

