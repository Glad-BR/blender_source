import bpy
from bl_ui.generic_ui_list import draw_ui_list

from .. import default_lods

# name = 0
# lod = 1
# arg = 2
# mode = 3

class DevLodListClass(bpy.types.PropertyGroup):
    
    name: bpy.props.StringProperty(default="LOD 10")
    lod: bpy.props.IntProperty(default=10)
    arg: bpy.props.IntProperty(default=10, min=0, max=100)

    mode_options = [
        ('OPTION1', "Collapse", "Collapse"),
        ('OPTION2', "Un-Subdivide", "Un-Subdivide"),
        ('OPTION3', "Planar", "Planar"),
    ]
    
    mode: bpy.props.EnumProperty(
        name="Mode",
        description="Choose a mode",
        items=mode_options,
        default='OPTION1'
    )


#=======================================================================================================================

def pannel_draw(layout, self, context):
    scene = context.scene
    
    dev_lod_list = scene.dev_lod_list
    index = scene.dev_lod_list_active_index
    
    box = layout.box().column()
    
    box.operator("object.reset_lod_list", text="Reset To Default")
    
    draw_ui_list(box, context, list_path="scene.dev_lod_list", active_index_path="scene.dev_lod_list_active_index", unique_id="dev_lod_list_id",)
    
    try:
        list_selected = dev_lod_list[index]
        
        colu = box.column(align=True)
        
        row1 = colu.row(align=True)
        row2 = colu.row(align=True)
        
        row1.prop(list_selected, "name")
        row1.prop(list_selected, "lod")
        
        row2.prop(list_selected, "mode")
        row2.prop(list_selected, "arg", text=string_lod_input_mode())
    
    except IndexError:
        None

#=======================================================================================================================

def string_lod_mode():
    scene = bpy.context.scene
    item = scene.dev_lod_list[scene.dev_lod_list_active_index]
    
    if item.mode == 'OPTION1': return "Collapse"
    if item.mode == 'OPTION2': return "Un-Subdivide"
    if item.mode == 'OPTION3': return "Planar"

def string_lod_input_mode():
    scene = bpy.context.scene
    item = scene.dev_lod_list[scene.dev_lod_list_active_index]
    
    if item.mode == 'OPTION1': return "Ratio"
    if item.mode == 'OPTION2': return "Iterations"
    if item.mode == 'OPTION3': return "Angle-Limit"

# name = 0
# lod = 1
# arg = 2
# mode = 3

def populate_default():
    
    scene = bpy.context.scene
    scene.dev_lod_list.clear()
    
    for index, [name, lod, arg, mode] in enumerate(default_lods):
        scene.dev_lod_list
        listy = scene.dev_lod_list.add()
        listy.name  = str(name)
        listy.lod   = int(lod)
        listy.arg   = int(arg)
        listy.mode  = str(mode)

#=======================================================================================================================

def get_legacy_list():
    
    scene = bpy.context.scene
    listy = scene.dev_lod_list
    
    legacy_list = []
    
    for item in listy:
        legacy_list.append([item.lod, item.arg])
    
    return legacy_list

def listUnpack():
    
    dev_lod_list = bpy.context.scene.dev_lod_list
    
    returnList = []
    
    for item in dev_lod_list:
        
        name = item.name
        lod  = item.lod
        arg  = item.arg
        mode = item.mode
        
        returnList.append([name, lod, arg, mode])
    
    return returnList

#=======================================================================================================================

class ResetLodList(bpy.types.Operator):
    bl_idname = "object.reset_lod_list"
    bl_label = "Add Enum Item"

    def execute(self, context):
        populate_default()
        return {'FINISHED'}

#=======================================================================================================================

classes = [
    DevLodListClass,
    ResetLodList,
]

class_register, class_unregister = bpy.utils.register_classes_factory(classes)


def register():
    class_register()
    bpy.types.Scene.dev_lod_list = bpy.props.CollectionProperty(type=DevLodListClass)
    bpy.types.Scene.dev_lod_list_active_index = bpy.props.IntProperty()


def unregister():
    class_unregister()
    del bpy.types.Scene.dev_lod_list
    del bpy.types.Scene.dev_lod_list_active_index