import os
import glob

# Auto-detect the most recent training output folder that contains the model configuration
output_base = "/content/gaussian-splatting/output"
cfg_files = glob.glob(f"{output_base}/*/cfg_args")

if cfg_files:
    # Get the most recently modified training output
    latest_cfg = max(cfg_files, key=os.path.getmtime)
    model_path = os.path.dirname(latest_cfg)
    print(f"Auto-detected latest model path from train.py: {model_path}")
else:
    print("Could not auto-detect model path. Make sure training completed successfully.")
    model_path = "./output/9b346ebd-7" # Fallback
