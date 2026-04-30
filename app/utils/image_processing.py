import os
import numpy as np
from PIL import Image, ImageDraw

def extract_tiles(image_path, tile_size=(256, 256)):
    """
    Simulates extracting tiles from a large image or WSI.
    For PoV, it slices a standard image into a grid.
    """
    try:
        img = Image.open(image_path)
        img_w, img_h = img.size
        
        tiles = []
        for x in range(0, img_w, tile_size[0]):
            for y in range(0, img_h, tile_size[1]):
                box = (x, y, x + tile_size[0], y + tile_size[1])
                tile = img.crop(box)
                tiles.append({
                    "coords": (x, y),
                    "tile": tile
                })
        return tiles, img.size
    except Exception as e:
        print(f"Error extracting tiles: {e}")
        return [], (0, 0)

def generate_mask(predictions, original_size, tile_size=(256, 256)):
    """
    Generates a color mask based on predictions.
    Colors: Tumor/CRC -> Red, Normal -> Green, Unknown -> Gray
    """
    mask = Image.new("RGBA", original_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(mask)
    
    for pred in predictions:
        x, y = pred["coords"]
        cls = pred["class"]
        
        if cls == "tumor":
            color = (255, 0, 0, 128) # Red, semi-transparent
        elif cls == "normal":
            color = (0, 255, 0, 128) # Green
        else:
            color = (128, 128, 128, 128) # Gray
            
        draw.rectangle([x, y, x + tile_size[0], y + tile_size[1]], fill=color)
        
    return mask

def overlay_mask(original_image_path, mask_image):
    """Overlays the generated mask onto the original image."""
    try:
        original = Image.open(original_image_path).convert("RGBA")
        combined = Image.alpha_composite(original, mask_image)
        return combined.convert("RGB")
    except Exception as e:
        print(f"Error overlaying mask: {e}")
        return None
