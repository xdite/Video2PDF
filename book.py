import os
import sys
from PIL import Image

# Check if the correct number of arguments is given
if len(sys.argv) != 3:
    print("Usage: python script.py <input_directory> <output_filename>")
    sys.exit(1)

input_directory = sys.argv[1]
output_file = sys.argv[2] + '.pdf'

# Collect all images
images = []

# Go through each PNG image in the directory
for filename in sorted(os.listdir(input_directory)):
    if filename.endswith(".png"):
        # Open the image file
        img = Image.open(os.path.join(input_directory, filename))
        # If image is not RGB, convert it to RGB
        if img.mode != "RGB":
            img = img.convert("RGB")
        images.append(img)

# Save all images to a single PDF file
if images:
    images[0].save(output_file, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])

print("Conversion from PNG to PDF is complete.")
