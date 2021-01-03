import os
import re
import shutil

input_dir = 'video'
output_dir = 'frame'
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

acceptable_extensions = ('mp4',)
index = 0

for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith(acceptable_extensions):
            output_subdir = os.path.join(output_dir, str(index))
            if not os.path.exists(output_subdir):
                os.makedirs(output_subdir)
            os.system(f'ffmpeg -i {os.path.join(root, file)} -r 1/1 {output_subdir}/%03d.png')
            index += 1
