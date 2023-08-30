import os
import threading

import bpy

from . import root_folder
from .GUI import tab0, tab1, tab2, tab3
from .misc import util


class SimplePanel(bpy.types.Panel):
    bl_label = "GBR Blender Source Tool"
    bl_idname = "OBJECT_PT_simple_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GBR Source"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        tab = scene.pannel_current_tab

        layout.label(text=f"Root @ {str(root_folder)}")
        
        tabs = layout.box().row(align=True)
        
        tabs.label(text="Auto convert and create vmt.")
        
        tabs.prop(scene, "multithreading", text="mat_multithreading")
        tabs.prop(scene, "vtf_multithreading", text="vtf_multithreading")
        
        tabz = tabs.row(align=True)
        tabz.scale_y = 1.4
        tabz.scale_x = 0.5
        
        tabz.operator("object.button0", text="MDL", depress=(tab == 0) )
        tabz.operator("object.button1", text="VTF", depress=(tab == 1) )
        tabz.operator("object.button2", text="VMT", depress=(tab == 2) )
        tabz.operator("object.button3", text="glTF", depress=(tab == 3) )
        
        layout.separator()
        
        if tab == 0:
            tab0.build(self, context)
        if tab == 1:
            tab1.build(self, context)
        if tab == 2:
            tab2.build(self, context)
        if tab == 3:
            tab3.build(self, context)
        #if tab == 4:
        #    tab4.build(self, context)
        

class TabOperator0(bpy.types.Operator):
    bl_idname = "object.button0"
    bl_label = "Button 0"
    def execute(self, context):
        context.scene.pannel_current_tab = 0
        return {'FINISHED'}

class TabOperator1(bpy.types.Operator):
    bl_idname = "object.button1"
    bl_label = "Button 1"
    def execute(self, context):
        context.scene.pannel_current_tab = 1
        return {'FINISHED'}

class TabOperator2(bpy.types.Operator):
    bl_idname = "object.button2"
    bl_label = "Button 2"
    def execute(self, context):
        context.scene.pannel_current_tab = 2
        return {'FINISHED'}

class TabOperator3(bpy.types.Operator):
    bl_idname = "object.button3"
    bl_label = "Button 3"
    def execute(self, context):
        context.scene.pannel_current_tab = 3
        return {'FINISHED'}

classes = [
    SimplePanel,
    TabOperator0,
    TabOperator1,
    TabOperator2,
    TabOperator3,
]

def register():
    
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.multithreading = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.vtf_multithreading = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.pil_multithreading = bpy.props.BoolProperty(default=False)
    
    bpy.types.Scene.pannel_current_tab = bpy.props.IntProperty(default=0, min=0, max=3)




def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.multithreading
    del bpy.types.Scene.vtf_multithreading
    del bpy.types.Scene.pil_multithreading