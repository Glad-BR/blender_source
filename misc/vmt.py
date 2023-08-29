import os

import bpy

from ..GUI import common
from . import path as ph


def to_bin(Input):
    if Input == True:
        Output = 1
    else:
        Output = 0
    return Output

def shrink_float_length(float_number, num_digits):
    format_string = f"{{:.{num_digits}f}}"
    formatted_number = format_string.format(float_number)
    return formatted_number



def main(scene, status, mat_name):
    
    Has_color, Has_pbr, Has_normal, Has_Light = status
    
    #Create VMT
    print("Creating VMT for Texture Name: "+str(mat_name))
    
    
    base_texture = str( os.path.join(ph.material(), mat_name) )
    surface_prop = scene.surfaceprop
    
    phongalbedotint = to_bin(scene.phongalbedotint)
    phongalbedoboost = scene.phongalbedoboost
    
    emissiveblendstrength = shrink_float_length(scene.light_power, 3)
    basealphaenvmapmask = to_bin(scene.basealphaenvmapmask)
    envmapfresnel = to_bin(scene.envmapfresnel)
    
    with open( os.path.join( ph.full_material() , mat_name+".vmt" ) , 'w') as f:
        f.write('"VertexLitGeneric"\n')
        f.write('{\n')
        f.write(f'\t"$basetexture"          "{base_texture}/Specular"   \n')
        if Has_normal:
            f.write(f'\t"$bumpmap"          "{base_texture}/Normal"     \n')
        f.write(f'\t"$surfaceprop"          "{surface_prop}"            \n')
        f.write(f'\t \n')
        
        if scene.use_phong and Has_pbr:
            f.write(f'\t"$phong"                "1"\n')
            #f.write(f'\t"$phongexponent"        "{scene.phongexponent}"\n')
            f.write(f'\t"$phongboost"           "{scene.phongboost}"\n')
            f.write(f'\t"$phongfresnelranges"   "{scene.phongfresnelranges}"\n')
            f.write(f'\t"$phongalbedotint" 	    "{phongalbedotint}"\n')
            f.write(f'\t"$phongalbedoboost" 	    "{phongalbedoboost}"\n')
            f.write(f'\t"$phongexponenttexture" "{base_texture}/Phong"\n')
            f.write(f'\t \n')
        
        #if Detail:
        #    f.write(f'\t"$detail"               "{base_texture}/Detail"\n')
        #    f.write(f'\t"$detailscale"          "1"\n')
        #    f.write(f'\t"$detailblendfactor"    "{shrink_float_length(scene.detailblendfactor, 3)}"\n')
        #    f.write(f'\t"$detailblendmode"      "{scene.detailblendmode}"\n')
        #    f.write(f'\t \n')

        if scene.use_env and Has_pbr:
            f.write(f'\t"$envmap"                   "env_cubemap"\n')
            f.write(f'\t"$envmaplightscale"		    "{scene.envmaplightscale}"\n')
            f.write(f'\t"$envmaplightscaleminmax"	"{scene.envmaplightscaleminmax}"\n')
            f.write(f'\t"$envmaptint"			    "{scene.envmaptint}"\n')
            f.write(f'\t"$envmapfresnel"		    "{envmapfresnel}"\n')
            f.write(f'\t"$basealphaenvmapmask"		"{basealphaenvmapmask}"\n')
            f.write(f'\t \n')
        
        if Has_Light:
            f.write(f'\t"$emissiveblendenabled"		    "1"\n')
            f.write(f'\t"$emissiveBlendBaseTexture"     "{base_texture}/Light"\n')
            f.write(f'\t"$EmissiveBlendFlowTexture"     "vgui/white"\n')
            f.write(f'\t"$EmissiveBlendTexture"         "vgui/white"\n')
            f.write(f'\t"$emissiveblendstrength"	    "{emissiveblendstrength}"\n')
            f.write(f'\t"$EmissiveBlendTint"		    "[1 1 1]"\n')
            f.write(f'\t"$EmissiveBlendScrollVector" 	"[0 0]"\n')
            f.write(f'\t \n')
        
        f.write(f'\t"$halflambert" "1" \n')
        f.write('}\n')