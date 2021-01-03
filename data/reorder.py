import os
from PIL import Image

input_dir = 'frame'
for root, dirs, files in os.walk(input_dir):
    if files:
        print(root)
    files.sort(key=lambda file: int(os.path.basename(file).split('.')[0]))
    for i, file in enumerate(files):
        extension = os.path.splitext(file)[-1]
        name = f'{i}{extension}'
        if file != name:
            old_file = os.path.join(root, file)
            Image.open(old_file).save(os.path.join(root, name))
            os.remove(old_file)
            