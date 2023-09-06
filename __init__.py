import logging as log
import os
import sys

import bpy

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

bl_info = {
    "name": "Blender Source Material & Model",
    "blender": (2, 80, 0),
    "category": "Object",
}

lod_num = [
    [25, 5],
    [50, 10],
    [75, 15]
]

pbr_channels = [
    ('red', "RED", "Red RGB Channel"),
    ('green', "GREEN", "Green RGB Channel"),
    ('blue', "BLUE", "Blue RGB Channel"),
]

root_folder = os.path.dirname(__file__)

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def check_pill():
    
    import subprocess
    
    try:
        import PIL
    except ImportError:
        # PIL is not installed, try to install it
        log.warn("PIL is not installed. Attempting to install...")

        try:
            subprocess.check_call([sys.executable, "-m", "ensurepip"])
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
            log.info("PIL (Pillow) has been successfully installed.")
        except subprocess.CalledProcessError:
            log.error("Failed to install PIL. Please install Pillow manually Into Blender Python Enviroment.")

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def register():
    
    check_pill()
    
    from . import GUI, main, misc
    GUI.register()
    main.register()
    misc.register()
    


def unregister():
    
    from . import GUI, main, misc
    GUI.unregister()
    main.unregister()
    misc.unregister()


if __name__ == "__main__":
    register()