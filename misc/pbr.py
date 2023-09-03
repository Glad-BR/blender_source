import os
import time

import bpy
from PIL import Image, ImageChops

from . import path as ph


def convert_to_pil(input_data):
    
    print("Converting Blender IMG to PIL")
    
    blender_image = input_data.image
    width, height = map(int, blender_image.size)
    num_channels = len(blender_image.pixels) // (width * height)
    mode = 'RGBA' if num_channels == 4 else 'RGB'
    pixel_data = [int(p * 255) for p in blender_image.pixels]
    pillow_image = Image.frombytes(mode, (width, height), bytes(pixel_data))
    return pillow_image



def load_img(node):
    path = os.path.abspath(bpy.path.abspath(node.image.filepath))
    print(f"Loading IMG: {os.path.basename(path)}")
    return Image.open(path)



def decode_pbr(pbr):
    scene = bpy.context.scene
    
    channel_images = {}
    channel_images['red'], channel_images['green'], channel_images['blue'] = pbr.split()
    
    dev = [
        "",
        f"roughness @ {scene.roughness_channel}_channel",
        f"metallic @ {scene.metallic_channel}_channel",
        f"ambient @ {scene.ambient_channel}_channel",
        ""
    ]
    for item in dev:
        print(item)
    
    roughness = channel_images.get(scene.roughness_channel, None)
    metallic = channel_images.get(scene.metallic_channel, None)
    ambient = channel_images.get(scene.ambient_channel, None)
    return roughness, metallic, ambient

def exponent(image, exponent):
    return Image.eval(image, lambda x: int(pow(x / 255.0, exponent) * 255))

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def pbr_magic(input_images):
    start_t = time.perf_counter()
    
    scene = bpy.context.scene
    image_color_input, image_normal_input, image_pbr = input_images

    color_original_size = image_color_input.size

    image_color = image_color_input.resize(image_pbr.size).convert("RGB")
    image_normal = image_normal_input.resize(image_pbr.size).convert("RGB")
    image_pbr = image_pbr.convert("RGB")
    
    roughness_map, metallic_map_in, ao_map = decode_pbr(image_pbr)
    
    metallic_map = ImageChops.invert(metallic_map_in) if scene.invert_metallic else metallic_map_in
    
    glossy_map = ImageChops.invert(roughness_map)
    
    
    if scene.use_metallic:
        print("Using Metallic Map in Color")
        spec2 = ImageChops.multiply(glossy_map, metallic_map)
        specular = ImageChops.multiply(image_color, spec2.convert('RGB'))
    else:
        print("Ignoring Metallic in Color")
        specular = ImageChops.multiply(image_color, glossy_map.convert('RGB'))
    
    
    if scene.use_ao:
        print("Using AO in Specular Texture")
        specular = ImageChops.multiply(specular, ao_map.convert('RGB'))
    
    if scene.normalmap_alpha_expo:
        image_normal.putalpha(exponent(glossy_map, 1.555))
    else:
        image_normal.putalpha(glossy_map)
    
    
    phong1 = exponent(glossy_map, 4.9)
    full_white = Image.new('L', image_pbr.size, 255)
    phong = Image.merge('RGB', (phong1.convert('L'), full_white, full_white))
    
    specular.putalpha(metallic_map)
    specular = specular.resize(color_original_size)
    
    print(f"PBR Magic Done in {int(time.perf_counter() - start_t)}s")
    return [specular, image_normal, phong], image_color

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def main(scene, nodes, status, material):
    has_color, has_pbr, has_normal, has_light = status
    
    work_folder = os.path.join( ph.full_material(), material.name)
    os.makedirs(work_folder, exist_ok=True)
    
    color = load_img(nodes[0])
    
    if has_pbr:
        pbr = load_img(nodes[1])
    if has_normal:
        normal = load_img(nodes[2])
    if has_light:
        light = load_img(nodes[3])
    
    
    print("Color:", has_color)
    print("PBR:", has_pbr)
    print("Normal:", has_normal)
    print("Emissive:", has_light)
    print("")
    print("use_phong:", scene.use_phong)
    print("use_env:", scene.use_env)
    print("use_metallic:", scene.use_metallic)
    print("")
    
    if has_color and has_pbr and has_normal:
        print("Using Regular PBR Export")
        
        input_images = [color, normal, pbr]
        output_images, raw_color = pbr_magic(input_images)
        
        for output_img, img_name in zip(output_images, ["Specular.png", "Normal.png", "Phong.png"]):
            output_img.save(os.path.join(work_folder, img_name))
    
    
    if has_light:
        light_out = light.resize(color.size).convert("RGB")
        
        if has_pbr and scene.light_mask_mode:
            light_out = ImageChops.multiply(raw_color, light_out)
        
        light_out.save(os.path.join(work_folder, "Light.png"))
    
    
    if not has_pbr:
        print("Using Fallback Export")
        color.save(os.path.join(work_folder, "Specular.png"))
        if has_normal:
            normal.save(os.path.join(work_folder, "Normal.png"))
