from glob import glob
from PIL import Image
from PIL import Image
from glob import glob
import cv2
import numpy as np

files = glob("images/webp/*")
for file in files:
    img = Image.open(file)
    img.save(file[:7]+"png/"+file[12:-5]+".png")

width = None
height = None

files = glob("images/png/*")
for file in files:
    name = file[11:-4]
    img = Image.open(file)
    img = np.array(img)
    if name=="ドラキー" or name=="ボストロール":
        width = 130
    else:
        width = 90
    height = 90
    img = cv2.resize(img, dsize=[width, height])
    img = Image.fromarray(img)
    save_path = f"images/png_resized/{name}_resized.png"
    img.save(save_path)