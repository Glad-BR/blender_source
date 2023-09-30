import logging as log
import os

import bpy

from ..GUI import common, ui_list
from . import path as ph

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def rem_decimate(obj):
    modifier = obj.modifiers.get("Decimate")
    if modifier:
        obj.modifiers.remove(modifier)

#Method 1
def add_decimate_edge_collapse(obj, in_data):
    rem_decimate(obj)
    
    modifier = obj.modifiers.new(name="Decimate", type='DECIMATE')
    modifier.decimate_type = 'COLLAPSE'
    modifier.ratio = (in_data / 100)

#Method 2
def add_decimate_unsubdivide(obj, in_data):
    rem_decimate(obj)
    
    modifier = obj.modifiers.new(name="Decimate", type='DECIMATE')
    modifier.decimate_type = 'UNSUBDIV'
    modifier.iterations = in_data

#Method 3
def add_decimate_planar(obj, in_data):
    rem_decimate(obj)
    
    modifier = obj.modifiers.new(name="Decimate", type='DECIMATE')
    modifier.decimate_type = 'DISSOLVE'
    modifier.angle_limit = in_data * (3.14159 / 180.0)  # Convert degrees to radians

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def decode_coll(collection):
    if collection and collection.objects:
        objects_with_vertices = [obj for obj in collection.objects if obj.type == 'MESH']
        return objects_with_vertices
    return []

def make_smooth_obj(obj):
    if obj and obj.type == 'MESH':
        obj.data.shade_smooth()

def make_smooth_coll(collection):
    for obj in decode_coll(collection):
        make_smooth_obj(obj)


def make_lod(collection):
    
    original_name = collection.name
    
    dev_lod_list = ui_list.listUnpack()
    
    for [name, lod, arg, mode] in dev_lod_list:
        if mode == 1:
            print(f"Lod: {str(lod)} Using Collapse With Ratio: {str(arg)}")
        if mode == 2:
            print(f"Lod: {str(lod)} Using Un-Subdivide With {str(arg)} Iterations")
        if mode == 3:
            print(f"Lod: {str(lod)} Using Planar With Angle: {str(arg)}")
    
    
    for [name, lod, arg, mode] in dev_lod_list:
        
        make_smooth_coll(collection)
        
        for obj in decode_coll(collection):
            
            if mode == 1:
                add_decimate_edge_collapse(obj, arg)
            
            if mode == 2:
                add_decimate_unsubdivide(obj, arg)
            
            if mode == 3:
                add_decimate_planar(obj, arg)
        
        new_name = f"LOD_{str(lod)}"
        
        collection.name = new_name
        bpy.ops.export_scene.smd(collection=new_name, export_scene=False)
    
    for obj in decode_coll(collection):
        rem_decimate(obj)
    
    collection.name = original_name

def export(collection, name):
    
    original_name = collection.name #Get original name
    
    collection.name = name #Set new temp name
    bpy.ops.export_scene.smd(collection=name, export_scene=False) #i hate you
    
    collection.name = original_name #Set Original name back


#Utils /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def func_export_ref(collection):
    
    scene = bpy.context.scene
    
    path = os.path.join(ph.work_folder(), ph.path_compile_model())
    os.makedirs(path, exist_ok=True)
    
    old_format = scene.vs.export_format
    old_path = scene.vs.export_path
    
    scene.vs.export_format = scene.gbr_export_format
    scene.vs.export_path = str(path)
    
    
    if collection:
        if scene.make_smooth:
            make_smooth_coll(collection)
        
        if scene.make_lods:
            make_lod(collection)
        
        export(collection, "Reference")
    
    
    bpy.context.scene.vs.export_format = old_format
    bpy.context.scene.vs.export_path = old_path


def func_export_pys(collection):
    scene = bpy.context.scene
    
    path = os.path.join(ph.work_folder(), ph.path_compile_model())
    os.makedirs(path, exist_ok=True)
    
    old_format = scene.vs.export_format
    old_path = scene.vs.export_path
    
    scene.vs.export_format = scene.gbr_export_format
    scene.vs.export_path = str(path)
    
    if collection:
        make_smooth_coll(collection)
        export(collection, "PYS")
    
    bpy.context.scene.vs.export_format = old_format
    bpy.context.scene.vs.export_path = old_path