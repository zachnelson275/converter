# utils/color_utils.py

import numpy as np
from PIL import Image

def rgb_to_hex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"

def closest_color(rgb, palette):
    return min(palette, key=lambda x: np.linalg.norm(np.array(rgb) - np.array(x[1])))

def convert_image_to_masks(image_path):
    image = Image.open(image_path).convert("RGB")
    img_array = np.array(image)
    h, w, _ = img_array.shape

    # Reshape for easier processing
    flat_pixels = img_array.reshape(-1, 3)
    
    # Identify unique colors directly in image
    unique_colors = np.unique(flat_pixels, axis=0)

    masks = []
    color_map = []

    for color in unique_colors:
        # Create mask where pixels match the color
        mask = np.all(img_array == color, axis=2).astype(np.uint8)
        masks.append(mask)
        color_map.append(tuple(color))

    return masks, color_map
