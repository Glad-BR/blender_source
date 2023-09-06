import logging as log
import os

import bpy

from ..GUI import common
from . import path as ph


def remove_decimate_modifier(obj):
    modifier = obj.modifiers.get("Decimate")
    if modifier:
        obj.modifiers.remove(modifier)

def add_decimate_modifier(obj, angle_limit_degrees):
    
    remove_decimate_modifier(obj)
    
    modifier = obj.modifiers.new(name="Decimate", type='DECIMATE')
    modifier.decimate_type = 'DISSOLVE'
    modifier.angle_limit = angle_limit_degrees * (3.14159 / 180.0)  # Convert degrees to radians

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


def make_lod(collection, lod_levels):
    
    original_name = collection.name
    
    for [lod_level, angle] in lod_levels:
        objects = decode_coll(collection)
        
        make_smooth_coll(collection)
        
        for obj in objects:
            log.info( obj.name+" With Lod: "+str(angle)+"Using Angle: "+str(angle) )
            
            add_decimate_modifier(obj, lod_level)
        
        new_name = "LOD_"+str(lod_level)
        
        collection.name = new_name
        bpy.ops.export_scene.smd(collection=new_name, export_scene=False)
    
    for obj in decode_coll(collection):
        remove_decimate_modifier(obj)
    
    collection.name = original_name

def export(collection, name):
    
    original_name = collection.name #Get original name
    
    collection.name = name #Set new temp name
    bpy.ops.export_scene.smd(collection=name, export_scene=False) #i hate you
    
    collection.name = original_name #Set Original name back


#Utils /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def func_export_ref(lod_num, collection):
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
            make_lod(collection, lod_num)
        
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