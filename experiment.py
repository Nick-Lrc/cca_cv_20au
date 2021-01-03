from vgg import VGGUtil
from PIL import Image, ImageFilter
import os
import shutil
import numpy as np
import numpy.linalg
import torch
import torch.nn as nn

input_dir = 'data/frame'
output_dir = 'result'
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)
log = open(os.path.join(output_dir, 'log.txt'), 'w')
neighbor_prob = .55  # 55% chance to pair with a neighbor on the right
model = VGGUtil(cuda=torch.cuda.is_available())
num_pairs = 200

imgs = set()
for root, dirs, files in os.walk(input_dir):
    for file in files:
        imgs.add(os.path.join(root, file))

counter = 0
while counter < num_pairs and len(imgs) > 1:
    print(counter)
    img = imgs.pop()
    index, ext = os.path.splitext(os.path.basename(img))
    root = img.rsplit(f'{os.path.sep}{index}', 1)[0]
    peer = os.path.join(root, f'{int(index) + 1}{ext}')
    if np.random.random() > neighbor_prob or peer not in imgs:
        peer = imgs.pop()
    else:
        imgs.remove(peer)
    entry = [img, peer]
    
    left = Image.open(img)
    right = Image.open(peer)

    try:
        left_blur = left.filter(ImageFilter.GaussianBlur())
        right_blur = right.filter(ImageFilter.GaussianBlur())

        left_sharp = left.filter(ImageFilter.UnsharpMask())
        right_sharp = right.filter(ImageFilter.UnsharpMask())

        left_gray = left.convert(mode='L').convert(mode='RGB')
        right_gray = right.convert(mode='L').convert(mode='RGB')

        left_gray_blur = left_gray.filter(ImageFilter.GaussianBlur())
        right_gray_blur = right_gray.filter(ImageFilter.GaussianBlur())

        left_gray_sharp = left_gray.filter(ImageFilter.UnsharpMask())
        right_gray_sharp = right_gray.filter(ImageFilter.UnsharpMask())

        pairs = [
            (left, right),
            (left_blur, right_blur),
            (left_sharp, right_sharp),
            (left_gray, right_gray),
            (left_gray_blur, right_gray_blur),
            (left_gray_sharp, right_gray_sharp)
        ]

        for pair in pairs:
            input1 = model.predict(pair[0])
            input2 = model.predict(pair[1])
            cos = nn.CosineSimilarity(dim=0)
            sim = cos(input1, input2).item()
            entry.append(str(sim))

        Image.fromarray(np.hstack([left, right.resize(left.size)])).save(os.path.join(output_dir, f'{counter}.png'))
        log.write(f'{",".join(entry)}\n')
    except Exception as e:
        counter -= 1
        print(e)
    finally:
        counter += 1
    