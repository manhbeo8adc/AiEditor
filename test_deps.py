import cv2
import torch
import flask
import numpy as np
from PIL import Image

print("✓ OpenCV version:", cv2.__version__)
print("✓ PyTorch version:", torch.__version__)
print("✓ CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("✓ GPU device:", torch.cuda.get_device_name(0))
print("✓ Flask version:", flask.__version__)
print("✓ NumPy version:", np.__version__)
print("All dependencies OK!") 