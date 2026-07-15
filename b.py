from pathlib import Path

dataset_path = Path("/workspace/Bonsaidownload")

print(f"Starting training on {dataset_path}...")

import subprocess

subprocess.run(
    [
        "python",
        "train.py",
        "-s",
        str(dataset_path),
        "--eval",
        "--iterations",
        "2000"
    ],
    check=True
)

print("\n--- Training Complete! ---")
print("Your model is saved under:")
print("output/<run_id>/point_cloud/iteration_2000/point_cloud.ply")
