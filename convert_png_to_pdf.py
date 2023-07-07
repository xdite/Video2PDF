import os
from PIL import Image
import shutil

def convert_png_to_pdf(input_directory, output_filename):
    output_file = output_filename + '.pdf'

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

    # Delete the directory
    try:
        shutil.rmtree(input_directory)
        print("Directory deleted successfully.")
    except OSError as e:
        print("Error: %s : %s" % (input_directory, e.strerror))

# To use the function:
# convert_png_to_pdf("/path/to/your/png/directory", "output_filename")
