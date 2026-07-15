import os
import glob

# RunPod path
output_base = "/workspace/gaussian-splatting/output"

# Find training outputs containing cfg_args
cfg_files = glob.glob(f"{output_base}/*/cfg_args")

if cfg_files:
    # Get newest training run
    latest_cfg = max(cfg_files, key=os.path.getmtime)

    # Model folder
    model_path = os.path.dirname(latest_cfg)

    print(f"Auto-detected latest model path:")
    print(model_path)

else:
    print("Could not find a trained model.")
    print("Check if training finished successfully.")

    model_path = None
