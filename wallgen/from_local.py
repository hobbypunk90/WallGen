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
        self.reset()

    def get_image(self, width=1920, height=1080, dark_mode=False)-> Image:
        while True:
            pos = randint(0, len(self.images)-1)
            if ((not dark_mode) or  __util__.is_dark_image(self.images[pos])) and (pos not in self.used_pos or len(self.used_pos) >= len(self.images)):
                break

        self.used_pos.append(pos)
        file_path = str(self.images[pos])
        return __util__.create_image(file_path, width, height)

    def reset(self):
        directory = re.compile('^~').sub(str(Path.home()), self.directory)
        self.images = []
        for pattern in self._types:
            self.images.extend(sorted(Path(directory).glob(pattern)))
        self.images.sort()
        self.used_pos = []