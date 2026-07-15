import os
import shutil
from PIL import Image

# Install xvfb for headless GPU OpenGL context
os.system("sudo apt-get install -y xvfb")

dataset_path = "/content/drive/MyDrive/nerf_datasets/bonsai"
input_path = os.path.join(dataset_path, "input")

# Ensure the 'input' folder exists
if not os.path.exists(input_path):
    os.makedirs(input_path)

print(f"Organizing 'input' directory at {input_path}")
valid_exts = ['.jpg', '.jpeg', '.png', '.exr', '.tif', '.tiff']

# 1. Move any valid images from the dataset root into 'input'
for item in os.listdir(dataset_path):
    if item == "input":
        continue
    item_path = os.path.join(dataset_path, item)
    if os.path.isfile(item_path):
        if any(item.lower().endswith(ext) for ext in valid_exts):
            shutil.move(item_path, os.path.join(input_path, item))

# 2. Move any NON-image files from 'input' back to the dataset root
for item in os.listdir(input_path):
    item_path = os.path.join(input_path, item)
    if os.path.isfile(item_path):
        if not any(item.lower().endswith(ext) for ext in valid_exts):
            print(f"Moving non-image file '{item}' out of 'input' folder...")
            shutil.move(item_path, os.path.join(dataset_path, item))

# 3. Limit to 40 images
all_images = sorted([f for f in os.listdir(input_path) if any(f.lower().endswith(e) for e in valid_exts)])
MAX_IMAGES = 40

if len(all_images) > MAX_IMAGES:
    print(f"\nFound {len(all_images)} images. Reducing to {MAX_IMAGES}...")
    for img in all_images[MAX_IMAGES:]:
        shutil.move(os.path.join(input_path, img), os.path.join(dataset_path, img))

images_count = len([f for f in os.listdir(input_path) if any(f.lower().endswith(e) for e in valid_exts)])
print(f"\nReady! Found {images_count} images in the 'input' folder.")

if images_count == 0:
    print("ERROR: No images found! Please check where your images are located in Google Drive.")
else:
    # 4. Resize images to prevent RAM crash
    print("\nResizing images to max 800px to prevent Colab from running out of RAM...")
    for img_name in os.listdir(input_path):
        if any(img_name.lower().endswith(e) for e in valid_exts):
            img_path = os.path.join(input_path, img_name)
            try:
                with Image.open(img_path) as img:
                    # Only resize if larger than 800
                    if img.size[0] > 800 or img.size[1] > 800:
                        img.thumbnail((800, 800), Image.Resampling.LANCZOS)
                        img.save(img_path)
            except Exception as e:
                print(f"Error resizing {img_name}: {e}")

    # 5. Clean up ANY broken folders from previous crashes
    distorted_path = os.path.join(dataset_path, "distorted")
    sparse_path = os.path.join(dataset_path, "sparse")

    if os.path.exists(distorted_path):
        shutil.rmtree(distorted_path)
        print("Cleaned up old interrupted 'distorted' database folder.")
    if os.path.exists(sparse_path):
        shutil.rmtree(sparse_path)
        print("Cleaned up old interrupted 'sparse' folder.")

    # Set the Qt platform to offscreen for headless Colab environment
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'

    # PATCH: Modify the convert.py script to use sequential_matcher instead of exhaustive_matcher
    print("\nPatching convert.py to use sequential_matcher...")
    !sed -i 's/exhaustive_matcher/sequential_matcher/g' convert.py

    # Run COLMAP with GPU using xvfb to provide a virtual display!
    print("\nStarting COLMAP extraction (GPU mode with xvfb) - Sequential Matching...")
    !xvfb-run python convert.py -s {dataset_path}
