import os
# -*- coding: utf-8 -*-
from subprocess import call

UPLOAD_PATH  = "/home/alokk/frp/frp/frp/static/uploads"

uploads_dir = os.path.join(UPLOAD_PATH, 'uploads')
size_1_dir = os.path.join(UPLOAD_PATH, 'size_1')
size_2_dir = os.path.join(UPLOAD_PATH, 'size_2')
img_prog = "mogrify"
for i in os.listdir(uploads_dir):
    orig_file = os.path.join(uploads_dir, i)
    orig_size = os.path.getsize(orig_file)
    print i + ' ' + str(orig_size)
    size_2_file = os.path.join(size_2_dir, i)
    size_2_size = os.path.getsize(size_2_file)
    print i + ' ' + str(size_2_size)
    if (size_2_size == orig_size):
        size_2_options = " -path %s -filter Triangle -define filter:support=2 \
                -thumbnail 300 -unsharp 0.25x0.08+8.3+0.045 -dither None -quality 82  \
                -define jpeg:fancy-upsampling=off -define png:compression-filter=5\
                -define png:compression-level=9 -define png:compression-strategy=1 \
                -define png:exclude-chunk=all -interlace none -colorspace sRGB \
                %s" %(size_2_dir, orig_file)
        print size_2_options
        size_2_cmd = img_prog + size_2_options
        call(size_2_cmd, shell=True)
