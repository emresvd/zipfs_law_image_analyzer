import argparse
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from collections import Counter
import os

def quantize_image(image, bits_per_channel):
    """
    Reduces the number of colors by quantizing each RGB channel.
    bits_per_channel: e.g., 2 bits means 4 values per channel (0, 85, 170, 255).
    """
    if bits_per_channel >= 8:
        return np.array(image)
        
    num_values = 2 ** bits_per_channel
    step = 256 / num_values
    
    img_array = np.array(image, dtype=np.float32)
    # Quantize
    quantized = np.floor(img_array / step) * step
    return quantized.astype(np.uint8)

def analyze_zipf_from_image(img, scale_factor=1.0, bits_per_channel=8):
    """
    Analyzes the image for Zipf's Law and generates a plot.
    Returns the matplotlib figure and the number of unique colors.
    """
    if scale_factor != 1.0:
        new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    # Quantize colors
    quantized_array = quantize_image(img, bits_per_channel)
    
    # Flatten array to list of RGB tuples
    pixels = quantized_array.reshape(-1, 3)
    pixel_tuples = [tuple(p) for p in pixels]
    
    # Count frequencies
    counter = Counter(pixel_tuples)
    
    # Sort frequencies in descending order
    frequencies = sorted(list(counter.values()), reverse=True)
    ranks = np.arange(1, len(frequencies) + 1)
    
    # Calculate Zipf reference line (y = C / x^a)
    # In pure Zipf's law, a = 1. C can be chosen as the max frequency.
    zipf_line = frequencies[0] / ranks
    
    fig = plt.figure(figsize=(10, 6))
    plt.loglog(ranks, frequencies, marker='o', linestyle='', markersize=4, label='Image Color Frequencies')
    plt.loglog(ranks, zipf_line, linestyle='--', color='red', label="Zipf's Law (1/f reference)")
    
    plt.title(f"Zipf's Law Analysis on Colors\nScale: {scale_factor}, Color Bits: {bits_per_channel}")
    plt.xlabel("Rank (Log Scale)")
    plt.ylabel("Frequency (Log Scale)")
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    
    return fig, len(frequencies)

def analyze_zipf(image_path, scale_factor=1.0, bits_per_channel=8, output_dir="."):
    print(f"Analyzing {image_path} with scale {scale_factor} and {bits_per_channel}-bit color depth...")
    img = Image.open(image_path).convert("RGB")
    fig, num_colors = analyze_zipf_from_image(img, scale_factor, bits_per_channel)
    
    # Save Plot
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    out_plot = os.path.join(output_dir, f"{base_name}_zipf_s{scale_factor}_b{bits_per_channel}.png")
    fig.savefig(out_plot)
    plt.close(fig)
    
    print(f"Analysis complete. Plot saved to {out_plot}")
    print(f"Total Unique Colors: {num_colors}")
    
    return out_plot

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze image colors for Zipf's Law")
    parser.add_argument("image", help="Path to the image file")
    parser.add_argument("--scale", type=float, default=1.0, help="Scale factor (e.g., 0.5 for half size)")
    parser.add_argument("--bits", type=int, default=8, help="Bits per color channel (1-8). Lower means fewer colors.")
    parser.add_argument("--outdir", default=".", help="Output directory for plots")
    
    args = parser.parse_args()
    analyze_zipf(args.image, scale_factor=args.scale, bits_per_channel=args.bits, output_dir=args.outdir)
