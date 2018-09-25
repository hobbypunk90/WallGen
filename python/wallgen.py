#!/usr/bin/python3
import os
import argparse

from pydbus import SessionBus
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib

from wallgen import WallGenDBUSService, Config

def main(args):
    config = Config()
    if not config.is_supported_desktop():
        raise Exception('Desktop environment not supported.')

    bus = SessionBus()
    loop = GLib.MainLoop()

    if args.dbus:
        bus.publish('de.thm.mni.mhpp11.WallGen', WallGenDBUSService(loop))
        run(loop)
    else:
        try:
            wg = bus.get('de.thm.mni.mhpp11.WallGen')
        except GLib.Error:
            wg = WallGenDBUSService(None)
        if type(wg) != WallGenDBUSService:
            if args.monitor:

                dc = None
                if config.is_gnome():
                    dc = bus.get('org.gnome.Mutter.DisplayConfig')
                elif config.is_kde():
                    dc = bus.get('org.kde.KScreen', object_path='/backend')
                with wg.Closed.connect(loop.quit):
                    if config.is_gnome():
                        with dc.MonitorsChanged.connect(wg.NewWallpaper):
                            run(loop)
                    elif config.is_kde():
                        class KDENewWallpaper:
                            first_call = True

                            def call(self, _):
                                if(self.first_call):
                                    wg.NewWallpaper()
                                self.first_call = not self.first_call

                        with dc.configChanged.connect(KDENewWallpaper().call):
                            run(loop)
            elif args.quit:
                wg.Close()
        elif type(wg) == WallGenDBUSService and args.monitor:
            raise Exception("Monitoring is not possible without DBus service!")
        if not args.monitor and not args.quit:
            wg.NewWallpaper()
        
    
def run(loop):
    try:
        loop.run()
    except KeyboardInterrupt:
        loop.quit()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Generates a random all screen spanning wallpaper from reddit or a directory. A large image is scaled down. A small image will get a background colored border.')

    parser.add_argument('-q', '--quit', action='store_true', default=False,
                        help='Stops the DBus service and if connected the monitor')

    parser.add_argument('--dbus', action='store_true', default=False,
                        help='Start as DBus service no other arguments are used!')
    parser.add_argument('--monitor', action='store_true', default=False,
                        help='Start as DBus monitor for changes at the monitor configuration')


    return parser.parse_args()


if __name__ == "__main__":
    main(parse_arguments())
    