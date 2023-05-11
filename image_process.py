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
    elif name[:5]=="主人公J3":
        width = 60
    else:
        width = 90
    if name[:5]=="主人公J3":
        height = 160
    elif name[:5]=="主人公IX":
        height = 140
    elif name[:7]=="主人公VIII":
        height = 160
    elif name[:5]=="主人公VI" and name[:6]!="主人公VII":
        height = 140
    elif name[:4]=="主人公V":
        height = 100
    elif name[:5]=="主人公IV":
        height = 140
    elif name[:3]=="主人公":
        # 主人公のデフォルトheight
        height = 120
    else:
        height = 90
    img = cv2.resize(img, dsize=[width, height])
    img = Image.fromarray(img)
    save_path = f"images/png_resized/{name}_resized.png"
    img.save(save_path)