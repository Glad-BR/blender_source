import logging as log
import os
import shutil
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
    
    box1 = layout.box().column()
    box1.prop(scene, "export_work_folder", text="Export Folder")
    
    row1 = box1.box().row(align=True)
    
    row1.prop(scene, "convert_vtf", text="Make VTF")
    row1.prop(scene, "make_vmt", text="Make VMT")
    row1.prop(scene, "del_modelsrc", text="Delete Modelscr")
    row1.prop(scene, "make_skin_groups", text="AutoEmissive Skin")
    
    funny3 = row1.row(align=True)
    funny3.scale_x = 0.65
    funny3.operator("wm.open_file_tex", text="VTF", icon='FILE_FOLDER')
    funny3.operator("wm.open_file_mdl", text="MDL", icon='FILE_FOLDER')
    funny3.operator("wm.open_file_qc", text="QC", icon='FILE_FOLDER')
    
    
    
    box1.label(text="Exporting to: "+str(ph.work_folder()) )
    
    row2 = box1.row(align=True)
    row2.scale_y = 1.3
    row2.operator("object.export_all", text="--->|Full Export|<---")
    row2.operator("object.tex_export", text="Export Textures")
    row2.operator("object.mesh_export", text="Export Model")
    row2.operator("object.open_hlmv", text="Open ModelVeiwer")
    


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def studio_ok():
    return os.path.exists(ph.studiomdl())

def hlmv_ok():
    return os.path.exists(ph.hlmv())

def lod_mode_string():
    scene = bpy.context.scene
    if scene.lod_mode == 1: return "Collapse"
    if scene.lod_mode == 2: return "Un-Subdivide"
    if scene.lod_mode == 3: return "Planar"

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Export_Texture(bpy.types.Operator):
    bl_idname = "object.tex_export"
    bl_label = "Export"
    def execute(self, context):
        scene = context.scene
        start_t = util.time_start()
        util.export_mat()
        self.report({'INFO'}, f"Done! in: {util.time_stop(start_t)}s")
        return {'FINISHED'}

class Export_Mesh(bpy.types.Operator):
    bl_idname = "object.mesh_export"
    bl_label = "Export Pys"
    def execute(self, context):
        if studio_ok():
            start_t = util.time_start()
            util.export_mesh()
            if bpy.context.scene.del_modelsrc:
                shutil.rmtree(os.path.join(ph.work_folder(),ph.path_compile_model()))
            self.report({'INFO'}, f"Done! in: {util.time_stop(start_t)}s")
        else: self.report({'INFO'}, "gameinfo.txt not found")
        return {'FINISHED'}

class Export_All(bpy.types.Operator):
    bl_idname = "object.export_all"
    bl_label = "Export All"
    def execute(self, context):
        if studio_ok():
            start_t = util.time_start()
            util.export_mat()
            util.export_mesh()
            if bpy.context.scene.del_modelsrc:
                shutil.rmtree(os.path.join(ph.work_folder(),ph.path_compile_model()))
            self.report({'INFO'}, f"Done! in: {util.time_stop(start_t)}s")
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

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class open_file_tex(bpy.types.Operator):
    bl_idname = "wm.open_file_tex"
    bl_label = "Open File Browser"
    def execute(self, context):
        path = os.path.join(ph.work_folder(),ph.path_material())
        if os.path.exists(path): bpy.ops.wm.path_open(filepath=path)
        else: self.report({'INFO'}, "VTF Folder Not Found")
        return {'FINISHED'}

class open_file_mdl(bpy.types.Operator):
    bl_idname = "wm.open_file_mdl"
    bl_label = "Open File Browser"
    def execute(self, context):
        path = os.path.join(ph.work_folder(),ph.path_model())
        if os.path.exists(path): bpy.ops.wm.path_open(filepath=path)
        else: self.report({'INFO'}, "MDL Folder Not Found")
        return {'FINISHED'}

class open_file_qc(bpy.types.Operator):
    bl_idname = "wm.open_file_qc"
    bl_label = "Open File Browser"
    def execute(self, context):
        path = os.path.join(ph.work_folder(),ph.path_compile_model())
        if os.path.exists(path): bpy.ops.wm.path_open(filepath=path)
        else: self.report({'INFO'}, "QC Folder Not Found")
        return {'FINISHED'}

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def runglmv():
    cmd = f'"{ph.hlmv()}" -game "{ph.source()}" -file "{ph.absolute_mdl()}"'
    target = os.path.join(ph.source(), "models")
    subprocess.run(cmd, shell=False, cwd=target)
    log.info(f"hlvm started with args: {cmd}")

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

classes = [
    Export_Texture,
    Export_Mesh,
    Export_All,
    open_hlmv,
    open_file_tex,
    open_file_mdl,
    open_file_qc,
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

    bpy.types.Scene.convert_vtf = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.make_vmt = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.make_skin_groups = bpy.props.BoolProperty(default=True)
    
    bpy.types.Scene.del_modelsrc = bpy.props.BoolProperty(default=False)
    
    
    bpy.types.Scene.lod_mode = bpy.props.IntProperty(default=1, max=3, min=1)

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.enable_display_mats
    
    del bpy.types.Scene.export_work_folder
    del bpy.types.Scene.source_root
    
    del bpy.types.Scene.model_path
    del bpy.types.Scene.material_path
    del bpy.types.Scene.model_name
    
    del bpy.types.Scene.surfaceprop
    
    del bpy.types.Scene.only_vmt
    del bpy.types.Scene.convert_vtf
    del bpy.types.Scene.make_vmt
    
    del bpy.types.Scene.make_skin_groups
    
    del bpy.types.Scene.del_modelsrc
    
    del bpy.types.Scene.lod_mode