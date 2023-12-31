import os

import bpy

from .. import save_file
from ..misc import path as ph
from ..misc import qc, smd, util
from . import common, tab01, tab3


def build(self, context):
    
    layout = self.layout
    scene = context.scene
    
    
    general_box(layout, scene)
    
    row1 = layout.box().row(align=True)
    #tab3.list_mats_box(row1, scene)
    tab01.draw(row1, self, context)
    draw_prop_config(row1, scene)
    
    box = layout.box()
    box.prop(scene, "ref_collection", text="Reference Collection")
    box.prop(scene, "pys_collection", text="Collision Collection")
    
    
    draw_formats(layout.box(), scene)
    
    draw_source_input(layout, scene)
    
    common.export_box(self, context)


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def general_box(layout, scene):
    
    box = layout.column(align=True)
    
    
    row = box.box().row(align=True)
    row.label(text="Prop Path Info")
    row.scale_x = 0.2
    row.operator("object.add_model_to_mat_string", text="Sync MAT to MDL")
    
    coll1 = box.box().column(align=True)
    coll1.prop(scene, "material_path", text="Materials/")
    coll1.prop(scene, "model_path", text="Models/")
    
    
    coll2 = box.box().column(align=True)
    coll2.prop(scene, "model_name", text="Model Name")
    coll2.prop(scene, "surfaceprop", text="surfaceprop")
    
    coll3 = box.box().column(align=True)
    coll3.prop(scene, "use_name_in_material", text= f"Use Name in Path | Full Material Path: [{str(ph.material())}]" )
    coll3.prop(scene, "use_name_in_model", text= f"Use Name in Path | Full Model Path:    [{str(ph.model())}]" )
    

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def draw_prop_config(layout, scene):
    
    box = layout.box().column()
    
    box.prop(scene, "staticprop", text="staticprop")
    
    box.prop(scene, "concave", text="concave")
    box.prop(scene, "contents", text="contents")
    
    box.prop(scene, "mass", text="mass")
    box.prop(scene, "inertia", text="inertia")


def draw_formats(layout, scene):
    
    row = layout.row(align=True)
    row.label(text="Export Format:")
    row.operator("object.dev_use_smd", text="SMD", depress=scene.gbr_export_format == 'SMD')
    row.operator("object.dev_use_dmx", text="DMX", depress=scene.gbr_export_format == 'DMX')
    
    row2 = layout.row(align=True)
    row2.prop(scene, "make_lods", text="Make LOD     Export:")
    row2.operator("object.export_auto", text="Export Mesh")
    row2.operator("object.make_qc", text="Write QC")
    row2.operator("object.compile_qc", text="Compile")
    row2.operator("wm.open_file_modelscr", text="", icon='FILE_FOLDER')



def draw_source_input(layout, scene):
    
    box = layout.box().column()
    
    box.prop(scene, "source_root", text="[gameinfo.txt] Path")
    
    row = box.row(align=True)
    row.operator("object.dev_dummy", text=f"studiomdl [{is_ok(ph.studiomdl())}]", depress=common.studio_ok())
    row.operator("object.dev_dummy", text=f"hlmv [{is_ok(ph.hlmv())}]", depress=common.hlmv_ok())
    

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def is_ok(path):
    if os.path.exists(path): return "OK"
    else: return "Not Found"

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class dev_use_smd(bpy.types.Operator):
    bl_idname = "object.dev_use_smd"
    bl_label = "Use SMD"
    def execute(self, context):
        scene = context.scene
        scene.gbr_export_format = 'SMD'
        return {'FINISHED'}

class dev_use_dmx(bpy.types.Operator):
    bl_idname = "object.dev_use_dmx"
    bl_label = "Use DMX"
    def execute(self, context):
        scene = context.scene
        scene.gbr_export_format = 'DMX'
        return {'FINISHED'}

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class export_auto(bpy.types.Operator):
    bl_idname = "object.export_auto"
    bl_label = "Export MDL"
    def execute(self, context):
        smd.func_export_ref(bpy.context.scene.ref_collection)
        smd.func_export_pys(bpy.context.scene.pys_collection)
        return {'FINISHED'}


class compile_qc(bpy.types.Operator):
    bl_idname = "object.compile_qc"
    bl_label = "Compile QC"
    def execute(self, context):
        util.run_studiomdl()
        return {'FINISHED'}

class make_qc(bpy.types.Operator):
    bl_idname = "object.make_qc"
    bl_label = "Make QC"
    def execute(self, context):
        qc.write_qc()
        qc.write_idle()
        return {'FINISHED'}

#///////////////////////////////////////////////////////////////////////////////

class add_model_to_mat_string(bpy.types.Operator):
    bl_idname = "object.add_model_to_mat_string"
    bl_label = "add_model_to_mat_string"
    def execute(self, context):
        scene = context.scene
        scene.material_path = os.path.normpath(os.path.join("models", scene.model_path))
        return {'FINISHED'}

#///////////////////////////////////////////////////////////////////////////////



#///////////////////////////////////////////////////////////////////////////////

class open_file_modelscr(bpy.types.Operator):
    bl_idname = "wm.open_file_modelscr"
    bl_label = "Open File Browser"
    def execute(self, context):
        path = os.path.join(ph.work_folder(),ph.path_compile_model())
        os.makedirs(path, exist_ok=True)
        bpy.ops.wm.path_open(filepath=path)
        return {'FINISHED'}



#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class dev_dummy(bpy.types.Operator):
    bl_idname = "object.dev_dummy"
    bl_label = "Open File Browser"
    def execute(self, context):
        return {'FINISHED'}

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

classes = [
    dev_use_smd,
    dev_use_dmx,
    export_auto,
    compile_qc,
    make_qc,
    add_model_to_mat_string,
    open_file_modelscr,
    dev_dummy
]



def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.gbr_export_format = bpy.props.StringProperty(default="DMX", description="gbr_export_format")
    
    bpy.types.Scene.ref_collection = bpy.props.PointerProperty(type=bpy.types.Collection)
    bpy.types.Scene.pys_collection = bpy.props.PointerProperty(type=bpy.types.Collection)
    
    bpy.types.Scene.make_lods = bpy.props.BoolProperty(default=True)
    
    bpy.types.Scene.make_smooth = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.pys_smooth = bpy.props.BoolProperty(default=True)
    
    
    bpy.types.Scene.use_name_in_model = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.use_name_in_material = bpy.props.BoolProperty(default=False)
    
    
    bpy.types.Scene.staticprop = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.contents = bpy.props.StringProperty(default="solid")
    
    bpy.types.Scene.mass = bpy.props.IntProperty(default=100)
    bpy.types.Scene.inertia = bpy.props.IntProperty(default=1)
    bpy.types.Scene.concave = bpy.props.BoolProperty(default=True)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.gbr_export_format
    
    del bpy.types.Scene.ref_collection
    del bpy.types.Scene.pys_collection
    
    del bpy.types.Scene.make_lods
    
    del bpy.types.Scene.make_smooth
    del bpy.types.Scene.pys_smooth
    
    del bpy.types.Scene.use_name_in_model
    del bpy.types.Scene.use_name_in_material
    
    del bpy.types.Scene.staticprop
    del bpy.types.Scene.contents
    
    del bpy.types.Scene.mass
    del bpy.types.Scene.inertia
    del bpy.types.Scene.concave
