import json
import os
import sys

import bpy

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

bl_info = {
    "name": "Blender Source Material & Model",
    "blender": (2, 80, 0),
    "category": "Object",
}

#default_lod_num = [
#    [25, 70],
#    [50, 50],
#    [75, 30],
#    [100, 18],
#]

default_lods = [
    ["LOD1", 25, 70, 'OPTION1'],
    ["LOD2", 50, 50, 'OPTION1'],
    ["LOD3", 75, 30, 'OPTION1'],
    ["LOD4", 100, 18, 'OPTION1'],
]

pbr_channels = [
    ('red', "RED", "Red RGB Channel"),
    ('green', "GREEN", "Green RGB Channel"),
    ('blue', "BLUE", "Blue RGB Channel"),
]

PopulateOnRegister = True

root_folder = os.path.dirname(__file__)

save_file = os.path.join(root_folder, "lod_lists.json")

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def check_pill():
    
    import subprocess
    
    try:
        import PIL
    except ImportError:
        print("PIL is not installed. Attempting to install...")
        try:
            subprocess.check_call([sys.executable, "-m", "ensurepip"])
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
            print("PIL (Pillow) has been successfully installed.")
        except subprocess.CalledProcessError:
            print("Failed to install PIL. Please install Pillow manually Into Blender Python Enviroment.")

# Save the list to a JSON file
def save_json(filename, data):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    print("Saved To json")
    for item in data: print(f"Lod: {item[0]}, angle: {item[1]}")
    print("")

# Load the list from a JSON file
def load_json(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    
    print("Loaded From json")
    for item in data: print(f"Lod: {item[0]}, angle: {item[1]}")
    print("")
    return data


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def register():
    
    check_pill()
    
    print("")
    print(f"Loading Addon {bl_info['name']}")
    print("By Glad_BR")
    print(f"Addon Root @ {root_folder}")
    print("")
    
    
    #if os.path.exists(save_file):
    #    global lod_num
    #    lod_num = load_json(save_file)
    #    print(f"LOD list loaded from {os.path.basename(save_file)}")
    #else:
    #    print(f"LOD list not found, created new file: {os.path.basename(save_file)}")
    #    save_json(save_file, default_lod_num)
    
    
    
    
    from . import GUI, main, misc
    GUI.register()
    main.register()
    misc.register()


def unregister():
    
    from . import GUI, main, misc
    GUI.unregister()
    main.unregister()
    misc.unregister()
    
    
    #global lod_num
    #save_json(save_file, lod_num)


if __name__ == "__main__":
    
    register()
    
    if PopulateOnRegister:
        from GUI import ui_list
        ui_list.populate_default()