#!/usr/bin/python3

import re
from gi.repository import GLib
from random import randint
from pathlib import Path
from wand.image import Image
from wallgen import __util__


types = ('*.jpg', '*.jpeg', '*.png')

def get_image(directory='{}/Wallpapers'.format(GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES)), width=1920, height=1080)-> Image:
    directory = re.compile('^~').sub(str(Path.home()), directory)
    list = []
    for pattern in types:
        list += sorted(Path(directory).glob(pattern))
    list.sort()
    pos = randint(0, len(list)-1)
    file_path = str(list[pos])
    return __util__.create_image(file_path, width, height)