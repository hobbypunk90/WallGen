#!/usr/bin/python3

import re
from gi.repository import GLib
from random import randint
from pathlib import Path
from wand.image import Image
from wallgen import __util__

class LocalGenerator:
    def __init__(self, directory='{}/Wallpapers'.format(GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES))):
        self._types = ('*.jpg', '*.jpeg', '*.png')
        self.directory = directory

    def get_image(self, width=1920, height=1080)-> Image:
        directory = re.compile('^~').sub(str(Path.home()), self.directory)
        list = []
        for pattern in self._types:
            list += sorted(Path(directory).glob(pattern))
        list.sort()
        pos = randint(0, len(list)-1)
        file_path = str(list[pos])
        return __util__.create_image(file_path, width, height)