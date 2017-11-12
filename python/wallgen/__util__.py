import re
from pathlib import Path
import shutil

from wand.image import Image


def create_image(path, width, height):
    image = Image(filename=path)
    if (image.width >= width or image.height >= height):
        # breite ist maßgebend
        h = height
        w = width
        if (image.width / width < image.height / height):
            h = int(round(image.height / (image.width / width)))
        # höhe ist maßgebend
        else:
            w = int(round(image.width / (image.height / height)))
        
        image.resize(w, h)
        image.crop(width=width, height=height, gravity='center')
        return image
    else:
        outerImg =  Image(width=width, height=height, background=image[1][1])
        outerImg.format = image.format.lower()
        outerImg.composite(image, left=int((width - image.width) / 2), top=int((height - image.height) / 2))
        image.close()
        return outerImg


def save(image, output):
    with image.convert('png') as converted:
        output = re.compile('^~').sub(str(Path.home()), output)
        tmpfile = "/tmp/wallgen"
        converted.save(filename=tmpfile)
        shutil.move(tmpfile, output)
        


def add_default_arguments(parser, output_suffix):
    parser.add_argument('-W', '--width', metavar='W', type=int, nargs='?', default=1920, help='Sets the width.')
    parser.add_argument('-H', '--height', metavar='H', type=int, nargs='?', default=1080, help='Sets the height.')
    parser.add_argument('-o', '--out', metavar='FILE', type=str, nargs='?', default="~/Bilder/Wallpaper_{}.png".format(output_suffix),
                        help='Sets the output file')