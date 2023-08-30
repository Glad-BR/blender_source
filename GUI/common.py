import ast
import os
import subprocess
import threading

import bpy

from ..misc import path as ph
from ..misc import util

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def export_box(self, context):
    layout = self.layout
    scene = context.scene
    
    layout.separator()
    
    box1 = layout.box()
    box1.prop(scene, "export_work_folder", text="Export Folder")
    
    row1 = box1.row()
    row1.prop(scene, "only_vmt", text="Only Make Vmt")
    row1.prop(scene, "convert_vtf", text="Make VTF")
    row1.prop(scene, "make_vmt", text="Make VMT")
    
    box1.label(text="Exporting to: "+str(ph.work_folder()) )
    
    row2 = box1.row(align=True)
    #row2.prop(scene, "auto_deploy", text="Auto Deploy")
    row2.operator("object.export_all", text="Full Export")
    row2.operator("object.tex_export", text="Export Textures")
    row2.operator("object.mesh_export", text="Export Model")
    row2.operator("object.open_hlmv", text="Open ModelVeiwer")
    


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def str_to_list(input_string):
    try:
        integer_list = ast.literal_eval(input_string)
        
        if isinstance(integer_list, list) and all(isinstance(item, int) for item in integer_list):
            return integer_list
        else:
            return None
    except (ValueError, SyntaxError):
        return None

def list_to_string(input_list):
    return ";".join(input_list)

def studio_ok():
    return os.path.exists(ph.studiomdl())

def hlmv_ok():
    return os.path.exists(ph.hlmv())

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Export_Texture(bpy.types.Operator):
    bl_idname = "object.tex_export"
    bl_label = "Export"
    def execute(self, context):
        scene = context.scene
        print("Beginning Exporting")
        util.export(scene)
        self.report({'INFO'}, "Exporting Textures")
        return {'FINISHED'}

class Export_Mesh(bpy.types.Operator):
    bl_idname = "object.mesh_export"
    bl_label = "Export Pys"
    def execute(self, context):
        if studio_ok():
            self.report({'INFO'}, "Exporting Model")
            util.export_mesh()
        else: self.report({'INFO'}, "gameinfo.txt not found")
        return {'FINISHED'}

class Export_All(bpy.types.Operator):
    bl_idname = "object.export_all"
    bl_label = "Export All"
    def execute(self, context):
        if studio_ok():
            self.report({'INFO'}, "Exporting Model & Textures")
            util.export(context.scene,)
            util.export_mesh()
            self.report({'INFO'}, "Export Complete")
        else: self.report({'INFO'}, "gameinfo.txt not found")
        return {'FINISHED'}


class open_hlmv(bpy.types.Operator):
    bl_idname = "object.open_hlmv"
    bl_label = "Open hlmv.exe"
    def execute(self, context):
        if hlmv_ok():
            thread = threading.Thread(target=runglmv)
            thread.start()
            self.report({'INFO'}, "hlmv started")
        else:
            self.report({'INFO'}, "hlmv Not Found")
        return {'FINISHED'}

def runglmv():
    scene = bpy.context.scene
    cmd = f'"{ph.hlmv()}" -game "{ph.source()}" -file "{os.path.join(ph.path_model(), scene.model_name)}.mdl"'
    subprocess.run(cmd, shell=False, cwd=os.path.join(ph.source(), "bin"))

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

classes = [
    Export_Texture,
    Export_Mesh,
    Export_All,
    open_hlmv
]

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.enable_display_mats = bpy.props.BoolProperty(default=True)
    
    bpy.types.Scene.export_work_folder = bpy.props.StringProperty(subtype="DIR_PATH", default="//export", description="Export Folder")
    
    bpy.types.Scene.source_root = bpy.props.StringProperty(subtype="DIR_PATH", default="//", description="gameinfo.exe path")
    
    
    bpy.types.Scene.model_path = bpy.props.StringProperty(default="my_model/path", description="Model Target Location")
    bpy.types.Scene.material_path = bpy.props.StringProperty(default='models/my_material_path/', description="path inside the materials folder")
    bpy.types.Scene.model_name = bpy.props.StringProperty(default='my_model_name', description="Model Name")
    
    bpy.types.Scene.surfaceprop = bpy.props.StringProperty(default='metal', description="surfaceprop")

    bpy.types.Scene.only_vmt = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.convert_vtf = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.make_vmt = bpy.props.BoolProperty(default=True)
    
    bpy.types.Scene.auto_deploy = bpy.props.BoolProperty(default=False)
    

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.enable_display_mats
    
    del bpy.types.Scene.export_work_folder
    del bpy.types.Scene.gameinfo_path
    
    del bpy.types.Scene.model_path
    del bpy.types.Scene.material_path
    del bpy.types.Scene.model_name
    
    del bpy.types.Scene.surfaceprop
    
    del bpy.types.Scene.only_vmt
    del bpy.types.Scene.convert_vtf
    del bpy.types.Scene.make_vmt
    
    del bpy.types.Scene.auto_deploy