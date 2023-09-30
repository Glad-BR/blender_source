import os

import bpy

from . import common, tab3, ui_list


def draw(layout, self, context):
    
    scene = context.scene
    
    tab = scene.tab0_subtab
    
    coll = layout.column(align=True)
    
    row = coll.row(align=True)
    row.operator("object.tab0_subtab_tab1", text="Materials", depress=(tab == 1))
    row.operator("object.tab0_subtab_tab2", text="Level Of Detail", depress=(tab == 2))
    
    if scene.tab0_subtab == 1:
        tab3.list_mats_box(coll, scene)
    if scene.tab0_subtab == 2:
        ui_list.pannel_draw(coll, self, context)


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class tab0_subtab_tab1(bpy.types.Operator):
    bl_idname = "object.tab0_subtab_tab1"
    bl_label = "Reset Node Labes"
    def execute(self, context):
        context.scene.tab0_subtab = 1
        return {'FINISHED'}

class tab0_subtab_tab2(bpy.types.Operator):
    bl_idname = "object.tab0_subtab_tab2"
    bl_label = "Reset Node Labes"
    def execute(self, context):
        context.scene.tab0_subtab = 2
        return {'FINISHED'}

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


classes = [
    tab0_subtab_tab1,
    tab0_subtab_tab2,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.tab0_subtab = bpy.props.IntProperty(default=1, max=2, min=1)




def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.tab0_subtab

