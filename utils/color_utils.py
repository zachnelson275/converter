# utils/color_utils.py

import numpy as np
from PIL import Image
import csv
import os

PALETTE_DIR = "palettes"

def load_palette_csv(palette_name):
    path = os.path.join(PALETTE_DIR, palette_name + ".csv")
    colors = []
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            r, g, b = int(row["R"]), int(row["G"]), int(row["B"])
            label = row.get("Name") or row.get("Label")
            colors.append((label, (r, g, b)))
    return colors

def closest_color(rgb, palette):
    return min(palette, key=lambda x: np.linalg.norm(np.array(rgb) - np.array(x[1])))

def convert_image_to_masks(image_path, palette_choice):
    image = Image.open(image_path).convert("RGB")
    img_array = np.array(image)
    h, w, _ = img_array.shape

    flat_pixels = img_array.reshape(-1, 3)
    palette = load_palette_csv(palette_choice)

    # Create a mapping from RGB → nearest palette color
    mapped_colors = np.array([closest_color(tuple(px), palette)[1] for px in flat_pixels])
    mapped_colors = mapped_colors.reshape((h, w, 3))

    # Find unique colors
    unique_colors = np.unique(mapped_colors.reshape(-1, 3), axis=0)

    masks = []
    color_map = []

    for color in unique_colors:
        mask = np.all(mapped_colors == color, axis=2).astype(np.uint8)
        masks.append(mask)
        color_map.append(tuple(color))

    return masks, color_map
