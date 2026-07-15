# Path to the Bonsai dataset in Google Drive
dataset_path = "/content/drive/MyDrive/nerf_datasets/bonsai"

print(f"Starting training on {dataset_path}...")
!python train.py -s {dataset_path} --eval --iterations 2000

print("\n--- Training Complete! ---")
print("To interactively view your 3D Gaussian Splatting model:")
print("1. Open the file browser on the left side of Colab.")
print("2. Navigate to the 'output' folder, find your latest run, and locate the .ply file: output/<run_id>/point_cloud/iteration_2000/point_cloud.ply")
print("3. Right-click the 'point_cloud.ply' file and select 'Download'.")
print("4. Open a web-based Gaussian Splat viewer in your browser, such as: https://antimatter15.com/splat/ or https://playcanvas.com/super-splat")
print("5. Drag and drop the downloaded .ply file into the webpage to explore your 3D model!")
