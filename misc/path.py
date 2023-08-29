import os

import bpy


def work_folder():
    scene = bpy.context.scene
    return os.path.normpath(bpy.path.abspath(scene.export_work_folder))

def material():
    scene = bpy.context.scene
    return os.path.normpath( os.path.join( scene.material_path, scene.model_name ) )

def model():
    scene = bpy.context.scene
    return os.path.normpath( os.path.join( scene.model_path, scene.model_name ) )

def source():
    scene = bpy.context.scene
    return os.path.normpath( bpy.path.abspath(scene.source_root) )


def studiomdl():
    return os.path.join( os.path.dirname(source()), "bin", "studiomdl.exe" )

def hlmv():
    return os.path.join( os.path.dirname(source()), "bin", "hlmv.exe" )

def path_material():
    return os.path.join( "materials", material() )

def path_model():
    return os.path.join( "models", model() )

def path_compile_model():
    return os.path.join( "modelsrc", model() )




def full_material():
    return os.path.join( work_folder(), path_material() )