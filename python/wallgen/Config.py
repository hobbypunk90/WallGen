import os

from yaml import load
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
        try:
            p = os.path.expanduser('~/.config/wallgen.yaml')
            with open(p) as stream:
                yaml = load(stream, Loader=Loader)
                params = {**params, **yaml}
        except Exception:
            pass
        self.type = params['type']
        self.subreddit = params['subreddit']
        self.directory = params['directory']
        self.output = params['output']
        self.generate_only = params['generate_only']
        self.disable_background = params['disable_background']
        self.disable_lockscreen = params['disable_lockscreen']

        self.desktop = os.environ['XDG_SESSION_DESKTOP'].lower()

    def is_supported_desktop(self):
        return self.desktop in ['gnome', 'kde']

    def is_gnome(self):
        return self.desktop == 'gnome'

    def is_kde(self):
        return self.desktop == 'kde'
