#!/usr/bin/env python3
"""
Gemini Watermark Remover - Reverse Alpha Blending Algorithm

Removes the "Generated with Gemini" watermark from Gemini AI-generated images.
Based on: https://github.com/GargantuaX/gemini-watermark-remover
"""

import sys
import base64
import struct
import argparse
from pathlib import Path

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Run: pip3 install pillow numpy")
    sys.exit(1)

SCRIPT_DIR = Path(__file__).parent

# Gemini watermark sizes and their margins from bottom-right corner
WATERMARK_CONFIGS = {
    48: {"margin": 8},
    96: {"margin": 16},
}


def load_alpha_map(size):
    """Load a pre-computed alpha map from base64 file."""
    b64_path = SCRIPT_DIR / f"alpha_{size}.b64"
    if not b64_path.exists():
        return None

    with open(b64_path, 'r') as f:
        b64_data = f.read().strip()

    decoded = base64.b64decode(b64_data)
    floats = []
    for i in range(0, len(decoded), 4):
        floats.append(struct.unpack('f', decoded[i:i+4])[0])
    return floats


def remove_watermark(image_path, output_path=None, verbose=False):
    """Remove Gemini watermark from an image using reverse alpha blending."""
    img = Image.open(image_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    width, height = img.size

    # Determine which watermark size to use based on image dimensions
    # Gemini uses 96px watermark for larger images, 48px for smaller
    if width >= 1024 or height >= 1024:
        wm_size = 96
    else:
        wm_size = 48

    margin = WATERMARK_CONFIGS[wm_size]["margin"]

    # Calculate watermark position (bottom-right corner)
    x = width - margin - wm_size
    y = height - margin - wm_size

    if verbose:
        print(f"Image: {width}x{height}")
        print(f"Watermark size: {wm_size}x{wm_size}, margin: {margin}")
        print(f"Watermark position: ({x}, {y})")

    # Load alpha map
    alpha_map = load_alpha_map(wm_size)
    if alpha_map is None:
        print(f"ERROR: Could not load alpha map for size {wm_size}")
        print(f"  Expected file: {SCRIPT_DIR / f'alpha_{wm_size}.b64'}")
        return None

    if verbose:
        non_zero = sum(1 for a in alpha_map if a > 0.001)
        print(f"Alpha map loaded: {len(alpha_map)} values, {non_zero} non-zero")

    # Convert image to numpy array
    img_data = np.array(img)
    orig_data = img_data.copy()

    ALPHA_NOISE_FLOOR = 3.0 / 255.0
    ALPHA_THRESHOLD = 0.002
    MAX_ALPHA = 0.99
    LOGO_VALUE = 255.0

    # Reverse alpha blending for each pixel in the watermark region
    for row in range(wm_size):
        for col in range(wm_size):
            alpha_idx = row * wm_size + col
            raw_alpha = alpha_map[alpha_idx]

            # Remove low-level alpha noise from compressed background capture
            signal_alpha = max(0, raw_alpha - ALPHA_NOISE_FLOOR)
            if signal_alpha < ALPHA_THRESHOLD:
                continue

            pixel_x = x + col
            pixel_y = y + row

            if pixel_x >= width or pixel_y >= height:
                continue

            # Apply denoised alpha for inverse solve
            alpha = min(raw_alpha, MAX_ALPHA)
            one_minus_alpha = 1.0 - alpha
            if one_minus_alpha < 0.001:
                one_minus_alpha = 0.001

            r = float(img_data[pixel_y, pixel_x, 0])
            g = float(img_data[pixel_y, pixel_x, 1])
            b = float(img_data[pixel_y, pixel_x, 2])

            # Reverse alpha blending formula
            # watermarked = alpha * LOGO_VALUE + (1-alpha) * original
            # => original = (watermarked - alpha * LOGO_VALUE) / (1-alpha)
            r_orig = (r - alpha * LOGO_VALUE) / one_minus_alpha
            g_orig = (g - alpha * LOGO_VALUE) / one_minus_alpha
            b_orig = (b - alpha * LOGO_VALUE) / one_minus_alpha

            img_data[pixel_y, pixel_x, 0] = int(max(0, min(255, round(r_orig))))
            img_data[pixel_y, pixel_x, 1] = int(max(0, min(255, round(g_orig))))
            img_data[pixel_y, pixel_x, 2] = int(max(0, min(255, round(b_orig))))

    # Count modified pixels
    modified = np.sum(np.abs(orig_data[:, :, :3].astype(int) - img_data[:, :, :3].astype(int)) > 0)

    if verbose:
        print(f"Modified {modified} pixels in watermark region")

    # Convert back to RGBA and save
    img_data[:, :, 3] = 255

    result = Image.fromarray(img_data, 'RGBA')

    if output_path is None:
        p = Path(image_path)
        output_path = str(p.parent / f"{p.stem}_no_watermark{p.suffix}")

    result.save(output_path)
    print(f"Saved: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Remove Gemini watermark from images')
    parser.add_argument('input', help='Input image path')
    parser.add_argument('output', nargs='?', help='Output image path (optional)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed info')

    args = parser.parse_args()

    result = remove_watermark(args.input, args.output, verbose=args.verbose)
    if result is None:
        sys.exit(1)


if __name__ == '__main__':
    main()
