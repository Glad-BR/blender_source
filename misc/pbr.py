import concurrent.futures
import os

import bpy
import numpy as np
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

def decode_pbr(pbr, scene):
    channel_images = {}
    channel_images['red'], channel_images['green'], channel_images['blue'] = pbr.split()
    
    dev = [
        "",
        f"roughness_channel @ {scene.roughness_channel}",
        f"metallic_channel @ {scene.metallic_channel}",
        f"ambient_channel @ {scene.ambient_channel}",
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


def normalize(img):
    img_array = np.array(img)
    normalized_array = (img_array - np.min(img_array)) / (np.max(img_array) - np.min(img_array))
    normalized_img = Image.fromarray((normalized_array * 255).astype(np.uint8))

    return normalized_img

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def pbr_magic(input_images, scene):
    image_color_input, image_normal_input, image_pbr = input_images

    image_color = image_color_input.resize(image_pbr.size).convert("RGB").transpose(Image.FLIP_TOP_BOTTOM)
    image_normal = image_normal_input.resize(image_pbr.size).convert("RGB").transpose(Image.FLIP_TOP_BOTTOM)
    image_pbr = image_pbr.convert("RGB").transpose(Image.FLIP_TOP_BOTTOM)
    
    roughness_map, metallic_map_in, ao_map = decode_pbr(image_pbr, scene)
    
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
    
    specular.putalpha(metallic_map)
    
    phong1 = exponent(glossy_map, 4.9)
    full_white = Image.new('L', image_pbr.size, 255)
    phong = Image.merge('RGB', (phong1.convert('L'), full_white, full_white))
    
    return [specular, image_normal, phong], image_color

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def main(scene, nodes, status, material):
    has_color, has_pbr, has_normal, has_light = status
    
    threads = []
    
    color = convert_to_pil(nodes[0])
    
    if has_pbr:
        pbr = convert_to_pil(nodes[1])
    if has_normal:
        normal = convert_to_pil(nodes[2])
    
    work_folder = os.path.join( ph.full_material(), material.name)
    os.makedirs(work_folder, exist_ok=True)
    
    print("\nColor:", has_color)
    print("PBR:", has_pbr)
    print("Normal:", has_normal)
    print("Emissive:", has_light)
    #print("\nuse_ao:", scene.use_ao)
    print("use_phong:", scene.use_phong)
    print("use_env:", scene.use_env)
    print("use_metallic:", scene.use_metallic)
    print("")
    
    if has_color and has_pbr and has_normal:
        print("Using Regular PBR Export")
        
        input_images = [color, normal, pbr]
        output_images, raw_color = pbr_magic(input_images, scene)
        
        for output_img, img_name in zip(output_images, ["Specular.png", "Normal.png", "Phong.png"]):
            output_img.save(os.path.join(work_folder, img_name))
    
    if has_light:
        light = convert_to_pil(nodes[3])
        light_out = light.resize(color.size).convert("RGB").transpose(Image.FLIP_TOP_BOTTOM)
        
        if has_pbr and scene.light_mask_mode:
            light_out = ImageChops.multiply(raw_color, light_out)
        
        light_out.save(os.path.join(work_folder, "Light.png"))
    
    if not has_pbr:
        print("Using Fallback Export")
        color.save(os.path.join(work_folder, "Specular.png"))
        if has_normal:
            normal.save(os.path.join(work_folder, "Normal.png"))
