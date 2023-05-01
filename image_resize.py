from pprint import pprint
from PIL import Image
from glob import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

width = 90
height = 90

files = glob("images/png/*")
for file in files:
    name = file[11:-4]
    img = Image.open(file)
    img = np.array(img)
    img = cv2.resize(img, dsize=[width, height])
    img = Image.fromarray(img)
    save_path = f"images/png_resized/{name}_resized.png"
    img.save(save_path)