import os
from PIL import Image

cwd = os.getcwd()
x = 640
y = 640
q = 80

for file in os.listdir(cwd):
    if file.lower().endswith(('.jpg', '.png', '.jpeg')):
        with Image.open(file) as image:
            image = image.resize((x, y), Image.ANTIALIAS)
            image.save(file, 'JPEG', quality=q)
