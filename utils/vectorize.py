# utils/vectorize.py

import subprocess
import os
import uuid

def save_mask_as_pbm(mask, filepath):
    h, w = mask.shape
    with open(filepath, 'wb') as f:
        f.write(f'P4\n{w} {h}\n'.encode())
        packed = bytearray()
        for row in mask:
            row_bits = ''.join(['1' if pixel else '0' for pixel in row])
            # pad to multiple of 8 bits
            row_bits += '0' * ((8 - len(row_bits) % 8) % 8)
            packed.extend(int(row_bits[i:i+8], 2) for i in range(0, len(row_bits), 8))
        f.write(packed)

def run_potrace(pbm_path):
    svg_path = pbm_path.replace(".pbm", ".svg")
    subprocess.run(["potrace", pbm_path, "-s", "-o", svg_path], check=True)
    with open(svg_path, "r") as f:
        return f.read()

def extract_paths_from_svg(svg_content):
    import re
    return re.findall(r'<path[^>]*d="([^"]+)"', svg_content)

def vectorize_masks_to_svg(masks):
    paths_per_layer = []
    for i, mask in enumerate(masks):
        pbm_path = f"/tmp/{uuid.uuid4()}.pbm"
        save_mask_as_pbm(mask, pbm_path)
        svg_data = run_potrace(pbm_path)
        paths = extract_paths_from_svg(svg_data)
        paths_per_layer.append(paths)
        os.remove(pbm_path)
    return paths_per_layer
