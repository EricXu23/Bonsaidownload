import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image

# Dataset location on RunPod
dataset_path = Path("/workspace/Bonsaidownload")
input_path = dataset_path / "input"

print(f"Using dataset: {dataset_path}")
print(f"Input folder: {input_path}")

# Ensure input folder exists
input_path.mkdir(exist_ok=True)

valid_exts = [".jpg", ".jpeg", ".png", ".exr", ".tif", ".tiff"]

# 1. Move images from dataset root into input folder
for item in dataset_path.iterdir():
    if item.name == "input":
        continue

    if item.is_file() and item.suffix.lower() in valid_exts:
        print(f"Moving {item.name} into input/")
        shutil.move(str(item), str(input_path / item.name))


# 2. Remove non-image files from input folder
for item in input_path.iterdir():
    if item.is_file() and item.suffix.lower() not in valid_exts:
        print(f"Moving non-image file {item.name} out of input/")
        shutil.move(str(item), str(dataset_path / item.name))


# 3. Limit number of images
images = sorted(
    [f for f in input_path.iterdir()
     if f.suffix.lower() in valid_exts]
)

MAX_IMAGES = 40

if len(images) > MAX_IMAGES:
    print(f"Found {len(images)} images, keeping only {MAX_IMAGES}")

    for img in images[MAX_IMAGES:]:
        shutil.move(str(img), str(dataset_path / img.name))


# Count images
images = [
    f for f in input_path.iterdir()
    if f.suffix.lower() in valid_exts
]

print(f"Ready! Found {len(images)} images")


if len(images) == 0:
    raise Exception("No images found in input folder")


# 4. Resize images
print("Resizing images if needed...")

for img_path in images:
    try:
        with Image.open(img_path) as img:

            if img.width > 800 or img.height > 800:
                img.thumbnail(
                    (800, 800),
                    Image.Resampling.LANCZOS
                )

                img.save(img_path)

                print(
                    f"Resized {img_path.name}"
                )

    except Exception as e:
        print(
            f"Error resizing {img_path.name}: {e}"
        )


# 5. Remove previous COLMAP outputs
for folder in ["distorted", "sparse"]:

    path = dataset_path / folder

    if path.exists():
        shutil.rmtree(path)
        print(f"Removed old {folder}")


# 6. Patch convert.py
convert_file = dataset_path / "convert.py"

if convert_file.exists():

    print("Patching convert.py...")

    subprocess.run(
        [
            "sed",
            "-i",
            "s/exhaustive_matcher/sequential_matcher/g",
            str(convert_file)
        ],
        check=True
    )

else:
    print(
        "convert.py not found in Bonsaidownload folder."
    )

# Run COLMAP conversion using Gaussian Splatting convert.py

print("Starting COLMAP conversion...")

os.environ["QT_QPA_PLATFORM"] = "offscreen"

subprocess.run(
    [
        "xvfb-run",
        "-a",
        "python",
        "/workspace/gaussian-splatting/convert.py",
        "-s",
        str(dataset_path)
    ],
    check=True
)
