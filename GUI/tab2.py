import os

import bpy

from . import common


def build(self, context):
    
    layout = self.layout
    scene = context.scene
    
    vmt_box(layout, scene)
    
    #pbr_box(layout, scene)
    
    light_box(layout, scene)
    
    
    if scene.use_phong:
        phong_box(layout, scene)
    
    #detail_box(layout, scene)
    
    if scene.use_env:
        env_box(layout, scene)
    
    #the last
    common.export_box(self, context)


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def vmt_box(layout, scene):
    
    box = layout.box()
    box.label(text="VMT Config")
    
    coll1 = box.column(align=True)
    coll1.prop(scene, "material_path", text="$basetexture")
    #coll1.prop(scene, "model_target_location", text="Model Path")
    
    #box.prop(scene, "model_name", text="Model Name")
    
    
    
    
    #coll2 = box.column(align=True)
    #coll2.box().label(text= "Full Material Path: [ "+str(common.materials_local_path(scene))+" ]" )
    #coll2.box().label(text= "Full Material Path: [ "+str(common.models_local_path(scene))+" ]" )


def pbr_box(layout, scene):
    
    box3 = layout.box()
    
    row1 = box3.row(align=True)
    row1.label(text="Fake PBR Options")
    row1.operator("object.pbr_reset", text="", icon='FILE_REFRESH')
    
    row2 = box3.row(align=True)
    coll1 = row2.column(align=True)
    coll2 = row2.column(align=True)
    coll3 = row2.column(align=True)
    
    coll1.prop(scene, "use_ao", text="Bake AO in Specular")
    coll1.prop(scene, "normalmap_alpha_expo", text="Roughness Exponent")
    
    coll2.prop(scene, "use_metallic", text="Use Metallic in Specular")
    coll2.prop(scene, "invert_metallic", text="Invert Metallic Map")
    
    box5 = coll3.box()
    box5.prop(scene, "light_mask_mode", text="Use Emissive as SelfIlium mask")
    
    box4 = layout.box()
    row8 = box4.row(align=True)
    row8.prop(scene, "use_phong", text="Use Phong")
    row8.prop(scene, "use_env", text="Enable ENV-map")


def light_box(layout, scene):
    
    box = layout.box()
    coll = box.column(align=True)
    
    row = coll.row()
    row.label(text="Emissive Options")
    row.operator("object.light_reset", text="", icon='FILE_REFRESH')
    
    coll.prop(scene, "use_light", text="Use Emissive (if available)")
    coll.prop(scene, "light_power", text="Emission Power")


def phong_box(layout, scene):
    
    box5 = layout.box()
    
    row = box5.row()
    row.label(text="Phong Shading Options")
    row.operator("object.phong_reset", text="", icon='FILE_REFRESH')
    
    coll = box5.column(align=False)
    #coll.prop(scene, "phongexponent", text="phongexponent")
    coll.prop(scene, "phongboost", text="phongboost")
    coll.prop(scene, "phongfresnelranges", text="phongfresnelranges")
    coll.prop(scene, "phongalbedotint", text="phongalbedotint")
    coll.prop(scene, "phongalbedoboost", text="phongalbedoboost")


def detail_box(layout, scene):
    
    tempbox = layout.box()
    row1 = tempbox.row()
    row1.label(text="Roughness Detail Options")
    row1.operator("object.detail_reset", text="", icon='FILE_REFRESH')
    coll1 = tempbox.column(align=False)
    coll1.prop(scene, "detailblendfactor", text="detailblendfactor")
    coll1.prop(scene, "detailblendmode", text="detailblendmode")


def env_box(layout, scene):
    
    tempbox = layout.box()
    row = tempbox.row()
    row.label(text="EnvMap Options")
    row.operator("object.env_reset", text="", icon='FILE_REFRESH')
    coll1 = tempbox.column(align=False)
    coll1.prop(scene, "envmaplightscale", text="envmaplightscale")
    coll1.prop(scene, "envmaplightscaleminmax", text="envmaplightscaleminmax")
    coll1.prop(scene, "envmaptint", text="envmaptint")
    coll1.prop(scene, "envmapfresnel", text="envmapfresnel")
    coll1.prop(scene, "basealphaenvmapmask", text="basealphaenvmapmask")


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class pbr_reset(bpy.types.Operator):
    bl_idname = "object.pbr_reset"
    bl_label = "Reset PBR Options to default"

    def execute(self, context):
        
        scene = context.scene
        
        scene.use_ao = True
        scene.use_phong = True
        scene.use_env = True
        scene.use_metallic = False
        scene.invert_metallic = False
        scene.normalmap_alpha_expo = True
        scene.light_mask_mode = False
    
        self.report({'INFO'}, "Phong Settings Reseted")
        return {'FINISHED'}

class light_reset(bpy.types.Operator):
    bl_idname = "object.light_reset"
    bl_label = "Reset Emissive to default"

    def execute(self, context):
        
        scene = context.scene
        
        scene.use_light = True
        scene.light_power = 1.0
    
        self.report({'INFO'}, "Phong Settings Reseted")
        return {'FINISHED'}

class phong_reset(bpy.types.Operator):
    bl_idname = "object.phong_reset"
    bl_label = "Reset Phong to default"

    def execute(self, context):
        
        scene = context.scene
        
        #scene.phongexponent = 5.0
        scene.phongboost = 3.0
        scene.phongfresnelranges = '[3 5 10]'
        scene.phongalbedotint = True
        scene.phongalbedoboost = 2.0
    
        self.report({'INFO'}, "Phong Settings Reseted")
        return {'FINISHED'}

class detail_reset(bpy.types.Operator):
    bl_idname = "object.detail_reset"
    bl_label = "Reset Detail to default"

    def execute(self, context):
        
        scene = context.scene

        scene.detailblendfactor = 0.2
        scene.detailblendmode   = 1.0
        
        self.report({'INFO'}, "Detail Settings Reseted")
        return {'FINISHED'}


class env_reset(bpy.types.Operator):
    bl_idname = "object.env_reset"
    bl_label = "Reset VTF to default"

    def execute(self, context):
        
        scene = context.scene

        scene.envmaplightscale = 1.0
        scene.envmaplightscaleminmax = '[0 1.25]'
        scene.envmaptint = '[1 1 1]'
        scene.envmapfresnel = True
        scene.basealphaenvmapmask = True

        self.report({'INFO'}, "EnvMap Settings Reseted")
        return {'FINISHED'}


classes = [
    pbr_reset,
    light_reset,
    phong_reset,
    detail_reset,
    env_reset
]

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    
    bpy.types.Scene.use_ao = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.use_phong = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.use_env = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.use_metallic = bpy.props.BoolProperty(default=False)
    
    bpy.types.Scene.invert_metallic = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.normalmap_alpha_expo = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.light_mask_mode = bpy.props.BoolProperty(default=False)
    
    
    bpy.types.Scene.use_light = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.light_power = bpy.props.FloatProperty(default=1.0, description="light_power")
    
    
    #bpy.types.Scene.phongexponent = bpy.props.FloatProperty(default=5.0, description="phongexponent")
    bpy.types.Scene.phongboost = bpy.props.FloatProperty(default=3.0, description="phongboost")
    bpy.types.Scene.phongfresnelranges = bpy.props.StringProperty(default='[3 5 10]', description="phongfresnelranges")
    bpy.types.Scene.phongalbedotint = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.phongalbedoboost = bpy.props.FloatProperty(default=2.0, description="phongalbedoboost")
    
    
    bpy.types.Scene.detailblendfactor = bpy.props.FloatProperty(default=0.2, description="detailblendfactor")
    bpy.types.Scene.detailblendmode = bpy.props.FloatProperty(default=1.0, description="detailblendmode")
    
    
    bpy.types.Scene.envmaplightscale = bpy.props.FloatProperty(default=1.0, description="envmaplightscale")
    bpy.types.Scene.envmaplightscaleminmax = bpy.props.StringProperty(default='[0 1.25]', description="envmaplightscaleminmax")
    bpy.types.Scene.envmaptint = bpy.props.StringProperty(default='[1 1 1]', description="envmaptint")
    bpy.types.Scene.envmapfresnel = bpy.props.BoolProperty(default=True)
    bpy.types.Scene.basealphaenvmapmask = bpy.props.BoolProperty(default=True)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    
    del bpy.types.Scene.use_ao
    del bpy.types.Scene.use_phong
    del bpy.types.Scene.use_env
    del bpy.types.Scene.use_metallic
    
    del bpy.types.Scene.invert_metallic
    del bpy.types.Scene.normalmap_alpha_expo
    del bpy.types.Scene.light_mask_mode
    
    del bpy.types.Scene.use_light
    del bpy.types.Scene.light_power
    
    #del bpy.types.Scene.phongexponent
    del bpy.types.Scene.phongboost
    del bpy.types.Scene.phongfresnelranges
    del bpy.types.Scene.phongalbedotint
    del bpy.types.Scene.phongalbedoboost

    del bpy.types.Scene.detailblendfactor
    del bpy.types.Scene.detailblendmode

    del bpy.types.Scene.envmaplightscale
    del bpy.types.Scene.envmaplightscaleminmax
    del bpy.types.Scene.envmaptint
    del bpy.types.Scene.envmapfresnel
    del bpy.types.Scene.basealphaenvmapmask