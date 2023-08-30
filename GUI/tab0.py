import os

import bpy

from .. import lod_num
from ..misc import path as ph
from ..misc import qc, smd, util
from . import common, tab3


def build(self, context):
    
    layout = self.layout
    scene = context.scene
    
    
    general_box(layout, scene)
    
    row1 = layout.box().row(align=True)
    tab3.list_mats_box(row1, scene)
    #lod_list_box(row1, scene)
    draw_prop_config(row1, scene)
    
    box = layout.box()
    box.prop(scene, "ref_collection", text="Reference Collection")
    box.prop(scene, "pys_collection", text="Collision Collection")
    
    
    draw_formats(layout.box(), scene)
    
    
    draw_source_input(layout, scene)
    
    common.export_box(self, context)


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def general_box(layout, scene):
    box = layout.box()
    box.label(text="Prop Path Info")
    
    coll1 = box.column(align=True)
    coll1.prop(scene, "material_path", text="Materials/")
    coll1.prop(scene, "model_path", text="Models/")
    
    coll2 = box.column(align=True)
    coll2.prop(scene, "model_name", text="Model Name")
    coll2.prop(scene, "surfaceprop", text="surfaceprop")
    
    coll3 = box.column(align=True)
    coll3.prop(scene, "use_name_in_material", text= "Use Name in Path | Full Material Path: [ "+str(ph.material())+" ]" )
    coll3.prop(scene, "use_name_in_model", text= "Use Name in Path | Full Model Path:    [ "+str(ph.model())+" ]" )
    

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def lod_list_box(layout, scene):
    row = layout.row(align=True)
    box = row.box()
    coll1 = box.column(align=True)
    for [lod, ang] in lod_num:
        coll1.label(text="Lod: "+str(lod)+" With Angle: "+str(ang))

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def draw_path_in(layout, scene):
    
    box = layout.box()
    
    row = box.row(align=False)
    
    coll2 = row.column(align=True)
    coll2.prop(scene, "model_target_location", text="Model Location")
    coll2.prop(scene, "model_name", text="Model Name")
    
    box.box().label(text= "Full Material Path: [ "+str(common.models_local_path(scene))+" ]" )


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
    row2.operator("wm.open_file_browser", text="", icon='FILE')
    


def draw_prop_config(layout, scene):
    
    box2 = layout.box().column()
    
    #row1 = box2.row(align=True)
    row1 = box2
    
    row1.prop(scene, "staticprop", text="staticprop")
    row1.prop(scene, "concave", text="concave")
    
    row1.prop(scene, "contents", text="contents")
    
    row1.prop(scene, "mass", text="mass")
    row1.prop(scene, "inertia", text="inertia")
    


def draw_source_input(layout, scene):
    
    box = layout.box().column()
    
    box.prop(scene, "source_root", text="[gameinfo.txt] Path")
    box.label(text=ph.source())
    
    if os.path.exists(ph.studiomdl()):
        box.label( text="studiomdl: OK" )
    else:
        box.label( text="studiomdl: Not Found" )
    
    if os.path.exists(ph.hlmv()):
        box.label( text="hlmv: OK" )
    else:
        box.label( text="hlmv: Not Found" )

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



class export_auto(bpy.types.Operator):
    bl_idname = "object.export_auto"
    bl_label = "Export Pys"
    def execute(self, context):
        global lod_num
        scene = bpy.context.scene
        smd.func_export_ref(lod_num, scene.ref_collection)
        scene = bpy.context.scene
        smd.func_export_pys(scene.pys_collection)
        return {'FINISHED'}

class export_ref(bpy.types.Operator):
    bl_idname = "object.export_ref"
    bl_label = "Export"
    def execute(self, context):
        scene = bpy.context.scene
        global lod_num
        smd.func_export_ref(lod_num, scene.ref_collection)
        return {'FINISHED'}

class export_pys(bpy.types.Operator):
    bl_idname = "object.export_pys"
    bl_label = "Export Pys"
    def execute(self, context):
        scene = bpy.context.scene
        smd.func_export_pys(scene.pys_collection)
        return {'FINISHED'}


class compile_qc(bpy.types.Operator):
    bl_idname = "object.compile_qc"
    bl_label = "Export Pys"
    def execute(self, context):
        scene = bpy.context.scene
        util.run_exe()
        return {'FINISHED'}

class make_qc(bpy.types.Operator):
    bl_idname = "object.make_qc"
    bl_label = "Export Pys"
    def execute(self, context):
        qc.write_qc()
        qc.write_idle()
        return {'FINISHED'}

#///////////////////////////////////////////////////////////////////////////////

class OpenFileBrowserOperator(bpy.types.Operator):
    bl_idname = "wm.open_file_browser"
    bl_label = "Open File Browser"
    
    def execute(self, context):
        # Open the file browser to the specific path
        path = os.path.join(ph.work_folder(),ph.path_compile_model())
        os.makedirs(path, exist_ok=True)
        bpy.ops.wm.path_open(filepath=path)
        return {'FINISHED'}

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

classes = [
    dev_use_smd,
    dev_use_dmx,
    export_auto,
    export_ref,
    export_pys,
    compile_qc,
    make_qc,
    OpenFileBrowserOperator
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
    
    
    del bpy.types.Scene.staticprop
    del bpy.types.Scene.contents
    
    del bpy.types.Scene.mass
    del bpy.types.Scene.inertia
    del bpy.types.Scene.concave
