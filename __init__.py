
import os
import subprocess
import sys

import bpy

bl_info = {
    "name": "Blender Source Material & Model",
    "blender": (2, 80, 0),
    "category": "Object",
}

lod_num = [
    [15, 15],
    [30, 30],
    [40, 40]
]

root_folder = os.path.dirname(os.path.abspath(__file__))

def check_pill():
    try:
        import PIL
    except ImportError:
        # PIL is not installed, try to install it
        print("PIL is not installed. Attempting to install...")

        try:
            subprocess.check_call([sys.executable, "-m", "ensurepip"])
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
            print("PIL (Pillow) has been successfully installed.")
        except subprocess.CalledProcessError:
            print("Failed to install PIL. Please install Pillow manually Into Blender Python Enviroment.")

def register():
    
    check_pill()
    
    from . import GUI, main, misc
    main.register()
    misc.register()
    GUI.register()


def unregister():
    
    from . import GUI, main, misc
    main.unregister()
    misc.unregister()
    GUI.unregister()


if __name__ == "__main__":
    register()