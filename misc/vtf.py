import logging as log
import os
import subprocess
import threading
import time

import bpy

from .. import root_folder
from . import util


def main(scene, work_folder):
    start_t = time.perf_counter()
    
    VTFCmd_Path = os.path.normpath(os.path.join( root_folder, "bin", "VTFCmd.exe" ))
    
    tasks = []
    
    for filename in os.listdir(work_folder):
        if filename.lower().endswith(".png"):
            if scene.vtf_multithreading:
                thread = threading.Thread(target=run_vtf, args=(filename, work_folder, scene, VTFCmd_Path,))
                tasks.append(thread)
                thread.start()
            else:
                run_vtf(filename, work_folder, scene, VTFCmd_Path)
    
    if scene.vtf_multithreading:
        for thread in tasks:
            thread.join()
    
    
    end_t = time.perf_counter()
    total_duration = end_t - start_t
    print(f"VTF took {total_duration:.2f}s total")
    print("")


def run_vtf(filename, work_folder, scene, VTFCmd_Path):
    
    file = os.path.join(work_folder, filename)
    
    Clamp = scene.clamp
    clamp_width = scene.clamp_width
    clamp_height = scene.clamp_height
    DeletePNGafterVTF = scene.del_png

    # Determine format and alpha format based on filename
            #"Color.png": (scene.color_format, scene.color_alpha_format),
    format_mapping = {
        "Specular.png": (scene.specular_format, scene.specular_alpha_format),
        "Normal.png": (scene.normal_format, scene.normal_alpha_format),
        "Phong.png": (scene.phong_format, scene.phong_alpha_format)
    }

    if filename in format_mapping:
        format, alpha_format = format_mapping[filename]
    else:
        format, alpha_format = scene.light_format, scene.light_alpha_format

    # Construct the VTF command
    cmd = f'"{VTFCmd_Path}" -file "{file}" -output "{work_folder}" '
    
    if Clamp:
        cmd = cmd + f'-resize -rwidth {clamp_width} -rheight {clamp_height} '
    
    cmd = cmd + f'-format {format} -alphaformat {alpha_format} -mfilter Catrom -flag Anisotropic '
    
    if filename == "Normal.png":
        cmd = cmd + '-flag Normal '
    
    print("Converting:", filename)
    
    # Run the VTF command
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if DeletePNGafterVTF:
        os.remove(file)
    
    vtf_file = os.path.join(work_folder, util.replace_file_extension(filename, ".vtf"))
    
    if os.path.exists(vtf_file):
        print("File:", filename, "Converted - OK")
    else:
        print("Convert Failed, VTF File Not found")