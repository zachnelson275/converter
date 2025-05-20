# utils/svg_builder.py

import svgwrite
from color_utils import rgb_to_hex

def build_svg_from_paths(paths_per_layer, color_map, output_path, canvas_size=(1000, 1000)):
    dwg = svgwrite.Drawing(output_path, size=canvas_size)
    
    for paths, color in zip(paths_per_layer, color_map):
        layer = dwg.g(fill=rgb_to_hex(*color))
        for d in paths:
            layer.add(dwg.path(d=d))
        dwg.add(layer)

    dwg.save()
