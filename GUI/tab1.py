import bpy

from . import common, tab2


def build(self, context):
    
    layout = self.layout
    scene = context.scene
    
    tab2.vmt_box(layout, scene)
    
    tab2.pbr_box(layout, scene)
    
    vtf_box(layout, scene)
    
    layout.box().prop(scene, "del_png", text="Delete Origninal PNG After VTF Conversion")
    
    clamp_box(layout, scene)
    
    
    #the last
    common.export_box(self, context)




#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




def vtf_box(layout, scene):
    
    box2 = layout.box()
    row = box2.row()
    row.label(text="VTF Formats.")
    row.label(text="Color Channel.")
    row.label(text="Alpha Channel.")
    
    row2 = row.row(align=True)
    row2.scale_x = 0.5
    row2.operator("object.defaults_low", text="Low")
    row2.operator("object.defaults_med", text="Mid")
    row2.operator("object.defaults_high", text="High")

    row4 = box2.row(align=True)
    row4.prop(scene, "specular_format", text="Specular")
    row4.prop(scene, "specular_alpha_format", text="")
    
    #row3 = box2.row(align=True)
    #row3.prop(scene, "color_format", text="Detail")
    #row3.prop(scene, "color_alpha_format", text="")

    row5 = box2.row(align=True)
    row5.prop(scene, "normal_format", text="Normal")
    row5.prop(scene, "normal_alpha_format", text="")
    
    row6 = box2.row(align=True)
    row6.prop(scene, "phong_format", text="Phong")
    row6.prop(scene, "phong_alpha_format", text="")
    
    row7= box2.row(align=True)
    row7.prop(scene, "light_format", text="Emissive")
    row7.prop(scene, "light_alpha_format", text="")


def clamp_box(layout, scene):
    
    box = layout.box()
    
    col = box.column(align=True)
    
    row1 = col.row(align=True)
    row1.label(text="Clamp (must be a multiple of 4)")
    row1.label(text="  Height.")
    row1.label(text="  Width.")
    
    row2 = col.row(align=True)
    
    
    row2.prop(scene, "clamp", text="Clamp")
    row2.prop(scene, "clamp_height", text="")
    row2.prop(scene, "clamp_width", text="")

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class defaults_low(bpy.types.Operator):
    bl_idname = "object.defaults_low"
    bl_label = "Reset VTF to default"
    def execute(self, context):
        scene = context.scene
        
        scene.specular_format         = "DXT1"
        scene.specular_alpha_format   = "DXT5"
        scene.normal_format           = "DXT1"
        scene.normal_alpha_format     = "DXT5"
        scene.phong_format            = "DXT1"
        scene.phong_alpha_format      = "DXT5"
    
        self.report({'INFO'}, "VTF Settings Reseted")
        return {'FINISHED'}

class defaults_med(bpy.types.Operator):
    bl_idname = "object.defaults_med"
    bl_label = "Reset VTF to default"
    def execute(self, context):
        scene = context.scene
        
        scene.specular_format         = "DXT1"
        scene.specular_alpha_format   = "DXT1"
        scene.normal_format           = "DXT1"
        scene.normal_alpha_format     = "DXT1"
        scene.phong_format            = "DXT1"
        scene.phong_alpha_format      = "DXT5"
    
        self.report({'INFO'}, "VTF Settings Reseted")
        return {'FINISHED'}

class defaults_high(bpy.types.Operator):
    bl_idname = "object.defaults_high"
    bl_label = "Reset VTF to default"
    def execute(self, context):
        scene = context.scene
        
        scene.specular_format         = "DXT1"
        scene.specular_alpha_format   = "BGRA8888"
        scene.normal_format           = "BGRA8888"
        scene.normal_alpha_format     = "BGRA8888"
        scene.phong_format            = "BGRA8888"
        scene.phong_alpha_format      = "DXT5"
    
        self.report({'INFO'}, "VTF Settings Reseted")
        return {'FINISHED'}

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

classes = [
    defaults_low,
    defaults_med,
    defaults_high
]

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.specular_format = bpy.props.StringProperty(default="DXT1", description="specular_format")
    bpy.types.Scene.specular_alpha_format = bpy.props.StringProperty(default="BGRA8888", description="specular_alpha_format")
    
    bpy.types.Scene.normal_format = bpy.props.StringProperty(default="BGRA8888", description="normal_format")
    bpy.types.Scene.normal_alpha_format = bpy.props.StringProperty(default="BGRA8888", description="normal_alpha_format")
    
    bpy.types.Scene.phong_format = bpy.props.StringProperty(default="BGRA8888", description="phong_format")
    bpy.types.Scene.phong_alpha_format = bpy.props.StringProperty(default="DXT5", description="phong_alpha_format")
    
    bpy.types.Scene.light_format = bpy.props.StringProperty(default="DXT1", description="light_format")
    bpy.types.Scene.light_alpha_format = bpy.props.StringProperty(default="DXT5", description="light_alpha_format")
    
    
    bpy.types.Scene.clamp = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.clamp_height = bpy.props.StringProperty(default="1024", description="clamp_height")
    bpy.types.Scene.clamp_width = bpy.props.StringProperty(default="1024", description="clamp_width")
    
    bpy.types.Scene.del_png = bpy.props.BoolProperty(default=True)


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.specular_format
    del bpy.types.Scene.specular_alpha_format
    del bpy.types.Scene.normal_format
    del bpy.types.Scene.normal_alpha_format
    del bpy.types.Scene.phong_format
    del bpy.types.Scene.phong_alpha_format
    del bpy.types.Scene.light_format
    del bpy.types.Scene.light_alpha_format
    
    
    del bpy.types.Scene.clamp
    del bpy.types.Scene.clamp_height
    del bpy.types.Scene.clamp_width
    
    del bpy.types.Scene.del_png