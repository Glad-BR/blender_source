import bpy

from ..misc import util
from . import common


def build(self, context):
    
    layout = self.layout
    scene = context.scene
    
    
    phong_box(layout, scene)
    
    list_mats_box(layout, scene)
    
    #the last
    common.export_box(self, context)


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def phong_box(layout, scene):
    
    box4 = layout.box()
    row7 = box4.row(align=True)
    row7.label(text="glTF node scanner config.")
    row7.operator("object.node_label_reset", text="", icon='FILE_REFRESH')
    
    row8 = box4.column(align=True)
    row8.prop(scene, "color_node_label", text="Color Node Label")
    row8.prop(scene, "normal_node_label", text="Normal Node Label")
    row8.prop(scene, "pbr_node_label", text="PBR Node Label")
    row8.prop(scene, "light_node_label", text="Emissive Node Label")
    
    box4.separator()
    
    box4.label(text="PBR Texture Color Channel mapping.")
    coll2 = box4.column()
    coll2.prop(scene, "ambient_channel", text="Ambient Occlusion")
    coll2.prop(scene, "roughness_channel", text="Roughness")
    coll2.prop(scene, "metallic_channel", text="Metallic")


def list_mats_box(layout, scene):
    
    box2 = layout.box().column(align=True)
    rowrow = box2.row(align=True)
    rowrow.label(text="Active Materials:")
    rowrow.label(text="Found Textures:")
    
    row1 = box2.row(align=True)
    boxy2 = row1.box().column(align=True)
    
    for material in util.get_materials():
        
        nodes, status = util.decode_material_nodes(scene, material)
        
        row = boxy2.row(align=True)
        
        color, pbr, normal, light = nodes
        has_color, has_pbr, has_normal, has_light = status
        
        row.label(text=material.name)
        
        if has_color or has_pbr or has_normal or has_light:
            
            to_print = []
            
            if has_color:
                to_print.append("Color")
            if has_pbr:
                to_print.append("PBR")
            if has_normal:
                to_print.append("Normal")
            if has_light:
                to_print.append("Emissive")

            row69 = row.column().row(align=True)
            row69.label(text=str(to_print) )

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class node_label_reset(bpy.types.Operator):
    bl_idname = "object.node_label_reset"
    bl_label = "Reset Node Labes"

    def execute(self, context):
        
        scene = context.scene
        
        scene.color_node_label  = "BASE COLOR"
        scene.pbr_node_label    = "METALLIC ROUGHNESS"
        scene.normal_node_label = "NORMALMAP"
        
        scene.ambient_channel = 'red'
        scene.metallic_channel = 'blue'
        scene.roughness_channel = 'green'

    
        self.report({'INFO'}, "VTF Settings Reseted")
        return {'FINISHED'}


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

pbr_channels = [
    ('red', "RED", "Red RGB Channel"),
    ('green', "GREEN", "Green RGB Channel"),
    ('blue', "BLUE", "Blue RGB Channel"),
    
]


classes = [
    node_label_reset,
]


#DXT1
#DXT5
#BGRA8888

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.color_node_label = bpy.props.StringProperty(default="BASE COLOR", description="color_node_label")
    bpy.types.Scene.pbr_node_label = bpy.props.StringProperty(default="METALLIC ROUGHNESS", description="pbr_node_label")
    bpy.types.Scene.normal_node_label = bpy.props.StringProperty(default="NORMALMAP", description="normal_node_label")
    bpy.types.Scene.light_node_label = bpy.props.StringProperty(default="EMISSIVE", description="light_node_label")
    
    bpy.types.Scene.ambient_channel = bpy.props.EnumProperty( items=pbr_channels, default='red', description="ambient_channel")
    bpy.types.Scene.roughness_channel = bpy.props.EnumProperty( items=pbr_channels, default='green', description="roughness_channel")
    bpy.types.Scene.metallic_channel = bpy.props.EnumProperty( items=pbr_channels, default='blue', description="metallic_channel")



def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.color_node_label
    del bpy.types.Scene.pbr_node_label
    del bpy.types.Scene.normal_node_label
    del bpy.types.Scene.light_node_label
    
    del bpy.types.Scene.roughness_channel
    del bpy.types.Scene.metallic_channel
    del bpy.types.Scene.ambient_channel
    
