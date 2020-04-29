#!/usr/bin/env python
# -*- coding: utf-8 -*- #

#adds advanced dithering effect to images
# Copyright (C) 2018  Roel Roscam Abbing

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os, logging, imghdr
from pelican import signals
from bs4 import BeautifulSoup
logger = logging.getLogger(__name__)

try:
    from PIL import Image
    import hitherdither
    enabled = True
except:
    logging.warning("Unable to load PIL or hitherdither, disabling thumbnailer")
    enabled = False

DEFAULT_IMAGE_DIR = "images2"
DEFAULT_DITHER_DIR = "dithers"
DEFAULT_DITHER_ORIGINAL_DIR = "dithers_original"
DEFAULT_THRESHOLD = [96, 96, 96] # this sets the contrast of the final image, rgb
DEFAULT_TRANSPARENCY= False
DEFAULT_TRANSPARENT_COLOR = [(125,125,125)]
DEFAULT_DITHER_PALETTE = [(25,25,25), (75,75,75),(125,125,125),(175,175,175),(225,225,225),(250,250,250)] # 6 tone palette\
DEFAULT_DITHER_PALOURDE = [(160,42,150),(255,255,255)] # 6 tone palette\
#DEFAULT_DITHER_PALOURDE = [(247,185,45),(160,42,150),(39,57,88),(255,255,255)] # 6 tone palette\


DEFAULT_RESIZE_OUTPUT = True
DEFAULT_MAX_SIZE = (500,500)
DEFAULT_MAX_SIZE_ORIGINAL = (200,200)

#11 tone palette, heavier, more detail, less visible dither pattern
#[(0,0,0),(25,25,25),(50,50,50),(75,75,75),(100,100,100),(125,125,125),(150,150,150),(175,175,175),(200,200,200),(225,225,225),(250,250,250)]

#3 tone palette, lighter, heavier dithering effect
# [(0,0,0), (125,125,125), (250,250,250)]


def _image_path(pelican):
    return os.path.join(pelican.settings['PATH'],
        pelican.settings.get("IMAGE_PATH", DEFAULT_IMAGE_DIR)).rstrip('/')

def _out_path(pelican):
    return os.path.join(pelican.settings['OUTPUT_PATH'],
                         pelican.settings.get('DITHER_DIR', DEFAULT_DITHER_DIR))

def dither(pelican):
    global enabled
    if not enabled:
        return
#in and out path for pelican
    #in_path = _image_path(pelican)
    #out_path = _out_path(pelican)

#in and out for local generation
    in_path = os.path.join(os.getcwd(), "images2")
    out_path = os.path.join(os.getcwd(), "dithers")


    #transparency = pelican.settings.get("TRANSPARENCY",DEFAULT_TRANSPARENCY)
    transparency = DEFAULT_TRANSPARENCY

    if not os.path.exists(out_path):
        os.mkdir(out_path)

    for dirpath, _, filenames in os.walk(in_path):
        for filename in filenames:
            file_, ext = os.path.splitext(filename)
            fn= os.path.join(dirpath,filename)
            of = os.path.join(out_path, filename.replace(ext,'.png'))
            if not os.path.exists(of) and imghdr.what(fn):
                logging.debug("dither plugin: dithering {}".format(fn))

                img= Image.open(fn).convert('RGB')

                #resize = pelican.settings.get('RESIZE', DEFAULT_RESIZE_OUTPUT)
                resize = DEFAULT_RESIZE_OUTPUT

                if resize:
                    #image_size = pelican.settings.get('SIZE', DEFAULT_MAX_SIZE)
                    image_size =DEFAULT_MAX_SIZE
                    img.thumbnail(image_size, Image.LANCZOS)
            
                #palette = hitherdither.palette.Palette(pelican.settings.get('DITHER_PALETTE', DEFAULT_DITHER_PALETTE))
                palette = hitherdither.palette.Palette(DEFAULT_DITHER_PALETTE)
            
                #threshold = pelican.settings.get('THRESHOLD', DEFAULT_THRESHOLD)
                threshold = DEFAULT_THRESHOLD
            
                img_dithered = hitherdither.ordered.bayer.bayer_dithering(img, palette, threshold, order=8) #see hither dither documentation for different dithering algos

                img_dithered.save(of, optimize=True)
    #logging.debug(calculate_savings(in_path,out_path))

def resize(pelican):
    global enabled
    if not enabled:
        return

#in and out for local generation
    in_path = os.path.join(os.getcwd(), "images2")
    out_path_original = os.path.join(os.getcwd(), "dithers_vignette")

    transparency = DEFAULT_TRANSPARENCY

    if not os.path.exists(out_path_original):
        os.mkdir(out_path_original)

    for dirpath, _, filenames in os.walk(in_path):
        for filename in filenames:
            file_, ext = os.path.splitext(filename)
            fn= os.path.join(dirpath,filename)
            of = os.path.join(out_path_original, filename.replace(ext,'_vignette.png'))
            if not os.path.exists(of) and imghdr.what(fn):
                logging.debug("dither plugin: dithering {}".format(fn))

                img= Image.open(fn).convert('RGB')

                #resize = pelican.settings.get('RESIZE', DEFAULT_RESIZE_OUTPUT)
                resize = DEFAULT_RESIZE_OUTPUT

                if resize:
                    #image_size = pelican.settings.get('SIZE', DEFAULT_MAX_SIZE)
                    image_size =DEFAULT_MAX_SIZE_ORIGINAL
                    img.thumbnail(image_size, Image.LANCZOS)
                    img.save(of, optimize=True)


def parse_for_images(instance):
    #based on better_figures_and_images plugin by @dflock, @phrawzty,@if1live,@jar1karp,@dhalperi,@aqw,@adworacz
    #https://github.com/getpelican/pelican-plugins/blob/master/better_figures_and_images/better_figures_and_images.py
    global DEFAULT_IMAGE_DIR
    global DEFAULT_DITHER_DIR
    global enabled

    if not enabled:
        return

    image_dir = instance.settings.get("IMAGE_PATH", DEFAULT_IMAGE_DIR)
    dither_dir = instance.settings.get('DITHER_DIR', DEFAULT_DITHER_DIR)


    if instance._content is not None:
        content = instance._content
        soup = BeautifulSoup(content, 'html.parser')
        for img in soup(['img', 'object']):
            fn, ext = os.path.splitext(img['src'])
            if ext.startswith('.'):
                img['src'] = img['src'].replace(ext, '.png') 
            img['src'] = img['src'].replace(image_dir,dither_dir)
                # logger.debug('dither plugin: rewrote image source to {}'.format(img['src']))
        instance._content = soup.decode()



def register():
    signals.finalized.connect(dither)
    signals.content_object_init.connect(parse_for_images)


#dither("pelican");
resize("pelican")