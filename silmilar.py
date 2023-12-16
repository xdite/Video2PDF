from PIL import Image
import imagehash
import os

def remove_duplicate_images(image_folder, hash_size=12, sim_threshold=10):
    """
    Remove duplicate images in a folder based on image hashing.

    :param image_folder: Folder containing images to be checked.
    :param hash_size: Size of the hash, defaults to 8.
    :param sim_threshold: Similarity threshold for considering images as duplicates, defaults to 5.
    """
    hashes = {}
    duplicates = []

    for image_filename in os.listdir(image_folder):
        if image_filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_folder, image_filename)
            try:
                # Create a hash for each image
                with Image.open(image_path) as img:
                    temp_hash = imagehash.average_hash(img, hash_size)

                # Check if the hash already exists in the dictionary
                if temp_hash in hashes:
                    print(f"Duplicate found: {image_filename} is a duplicate of {hashes[temp_hash]}")
                    duplicates.append(image_path)
                else:
                    hashes[temp_hash] = image_filename

            except Exception as e:
                print(f"Error processing {image_filename}: {e}")

    # Optionally, remove the identified duplicate images
    for duplicate in duplicates:
        os.remove(duplicate)
        #print(f"Removed duplicate image: {duplicate}")
