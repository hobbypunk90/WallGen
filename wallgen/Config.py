import os

from yaml import load, dump
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from gi.repository import GLib


class Config(object):
    def __init__(self):
        params = {'type': 'local',
                  'subreddit': 'earthporn',
                  'directory': '{}/Wallpapers'.format(GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES)),
                  'output': GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES),
                  'generate_only': False,
                  'disable_background': False,
                  'disable_lockscreen': False
                }
        p = os.path.expanduser('~/.config/wallgen.yaml')
        try:
            with open(p) as stream:
                yaml = load(stream, Loader=Loader)
                params = {**params, **yaml}
        except Exception:
            with open(p, "w") as stream:
                dump(params, stream)
        self.type = params['type']
        self.subreddit = params['subreddit']
        self.directory = params['directory']
        self.output = params['output']
        self.generate_only = params['generate_only']
        self.disable_background = params['disable_background']
        self.disable_lockscreen = params['disable_lockscreen']

        self.desktop = os.environ['XDG_SESSION_DESKTOP'].lower()

    def is_supported_desktop(self):
        return self.desktop in ['gnome', 'gnome-xorg', 'kde']

    def is_gnome(self):
        return self.desktop in ['gnome','gnome-xorg'] 

    def is_kde(self):
        return self.desktop == 'kde'
