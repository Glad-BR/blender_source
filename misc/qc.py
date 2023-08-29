import os

import bpy

from .. import lod_num
from ..GUI import common
from . import path as ph


def build():
    write_qc()
    write_idle()

def write_qc():
    scene = bpy.context.scene
    
    model_name = str(scene.model_name)
    
    export_format = str.lower(scene.gbr_export_format)
    
    reference = "Reference"
    
    qc_path = os.path.join( ph.work_folder(), ph.path_compile_model())
    os.makedirs(qc_path, exist_ok=True)
    
    temp = os.path.join(qc_path, "compile.qc")
    
    with open( temp , 'w') as f:
        f.write('//Blender Source Addon\n')
        f.write('//Created By Glad_BR\n')
        f.write('\n')
        #Body
        if scene.staticprop:
            f.write('$staticprop\n')
        
        f.write('\n')
        f.write(f'$modelname "{ph.model()}.mdl"\n')
        
        f.write('\n')
        f.write('$bodygroup "Body"\n')
        f.write('{\n')
        f.write(f'\tstudio "{reference}.{export_format}"\n')
        f.write('}\n')
        f.write('\n')
        
        if scene.make_lods:
            for [lod, ang] in lod_num:
                f.write(f'$lod {lod}\n')
                f.write('{\n')
                f.write(f'\treplacemodel "{reference}.{export_format}" "LOD_{lod}.{export_format}"\n')
                f.write(f'\tnofacial\n')
                f.write('}\n')
                f.write('\n')
        
        f.write(f'$surfaceprop "{scene.surfaceprop}"\n')
        f.write('\n')
        f.write(f'$contents "{scene.contents}"\n')
        f.write('\n')
        f.write(f'$cdmaterials "{ph.material()}"\n')
        f.write('\n')
        
        f.write(f'$collisionmodel "PYS.{export_format}"\n')
        f.write('{\n')
        if scene.concave:
            f.write(f'\t$concave\n')
        
        f.write(f'\t$mass {str(scene.mass)}\n')
        f.write(f'\t$inertia {str(scene.inertia)}\n')
        
        f.write(f'\t$maxconvexpieces 10000\n')
        f.write('}\n')
        f.write('\n')
        
        f.write(f'$sequence "idle" "{os.path.join("anims","idle.SMD")}"\n')
        f.write('\n')

def write_idle():
    scene = bpy.context.scene
    
    
    qc_path = os.path.join( ph.work_folder(), ph.path_compile_model(), "anims")
    os.makedirs(qc_path, exist_ok=True)
    
    with open( str(os.path.join(qc_path, "idle.SMD")), 'w') as f:
        f.write('version 1\n')
        f.write('nodes\n')
        f.write('0 "Implicit" -1\n')
        f.write('end\n')
        f.write('skeleton\n')
        f.write('time 0\n')
        f.write('0  0.000000 0.000000 0.000000  0.000000 0.000000 0.000000\n')
        f.write('end\n')
        f.write('triangles\n')
        f.write('end\n')
