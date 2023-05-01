from glob import glob
from PIL import Image

files = glob("images/webp/*")
for file in files:
    img = Image.open(file)
    img.save(file[:7]+"png/"+file[12:-5]+".png")