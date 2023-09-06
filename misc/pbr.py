import logging as log
import os
import time

import bpy
from PIL import Image, ImageChops

from . import path as ph
from . import util


def convert_to_pil(input_data):
    blender_image = input_data.image
    width, height = map(int, blender_image.size)
    num_channels = len(blender_image.pixels) // (width * height)
    mode = 'RGBA' if num_channels == 4 else 'RGB'
    pixel_data = [int(p * 255) for p in blender_image.pixels]
    pillow_image = Image.frombytes(mode, (width, height), bytes(pixel_data))
    return pillow_image.transpose(Image.FLIP_TOP_BOTTOM)


def load_img(node):
    
    devmode = bpy.context.scene.devmode
    
    
    path = os.path.abspath(bpy.path.abspath(node.image.filepath))
    if devmode:
        log.info(f"path: {path}")
        log.info(os.path.exists(path))
    
    try:
        if devmode: log.info(f"Loading IMG: {os.path.basename(path)}")
        return Image.open(path)
    except FileNotFoundError:
        if devmode:
            log.info("Original File Not Found, Converting Existing Loaded IMG")
            log.info(f"Converting To Pil: {os.path.basename(path)}")
        return convert_to_pil(node)


def decode_pbr(pbr):
    scene = bpy.context.scene
    
    channel_images = {}
    channel_images['red'], channel_images['green'], channel_images['blue'] = pbr.split()
    
    if scene.devmode:
        dev = [
            "",
            f"roughness @ {scene.roughness_channel}_channel",
            f"metallic @ {scene.metallic_channel}_channel",
            f"ambient @ {scene.ambient_channel}_channel",
            ""
        ]
        for item in dev:
            log.info(item)
    
    roughness = channel_images.get(scene.roughness_channel, None)
    metallic = channel_images.get(scene.metallic_channel, None)
    ambient = channel_images.get(scene.ambient_channel, None)
    return roughness, metallic, ambient


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def exponent(image, exponent):
    return Image.eval(image, lambda x: int(pow(x / 255.0, exponent) * 255))

def pbr_magic(input_images):
    
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
        if scene.devmode: log.info("Using Metallic Map in Color")
        spec2 = ImageChops.multiply(glossy_map, metallic_map)
        specular = ImageChops.multiply(image_color, spec2.convert('RGB'))
    else:
        if scene.devmode: log.info("Ignoring Metallic in Color")
        specular = ImageChops.multiply(image_color, glossy_map.convert('RGB'))
    
    
    if scene.use_ao:
        if scene.devmode: log.info("Using AO in Specular Texture")
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
    
    return [specular, image_normal, phong], image_color

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def main(scene, nodes, status, material):
    has_color, has_pbr, has_normal, has_light = status
    
    work_folder = os.path.join( ph.full_material(), material.name)
    os.makedirs(work_folder, exist_ok=True)
    
    #load Images
    
    time_temp = util.time_start()
    
    if has_color: color = load_img(nodes[0])
    if has_pbr: pbr = load_img(nodes[1])
    if has_normal: normal = load_img(nodes[2])
    if has_light: light = load_img(nodes[3])

    
    #log.info("Color:", has_color)
    #log.info("PBR:", has_pbr)
    #log.info("Normal:", has_normal)
    #log.info("Emissive:", has_light)
    #log.info("")
    #log.info("use_phong:", scene.use_phong)
    #log.info("use_env:", scene.use_env)
    #log.info("use_metallic:", scene.use_metallic)
    #log.info("")
    
    if has_color and has_pbr and has_normal:
        #log.info("Using Regular PBR Export")
        
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
        log.info("Using Fallback Export")
        if has_color: color.save(os.path.join(work_folder, "Specular.png"))
        if has_normal: normal.save(os.path.join(work_folder, "Normal.png"))
    
    log.info(f"PBR Export Done in {util.time_stop(time_temp)}s")
