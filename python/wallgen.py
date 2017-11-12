#!/usr/bin/python3

from pydbus import SessionBus

import argparse

from gi.repository import GLib

from wallgen import WallGenDBUSService


def main(args):
    bus = SessionBus()
    loop = GLib.MainLoop()

    def new_wallpaper():
        wg.NewWallpaper(args.type, args.subreddit, args.directory, args.output, args.generate_only)
        
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
                dc = bus.get('org.gnome.Mutter.DisplayConfig')
                with wg.Closed.connect(loop.quit):
                    with dc.MonitorsChanged.connect(new_wallpaper):
                        run(loop)
            elif args.quit:
                wg.Close()
        elif type(wg) == WallGenDBUSService and args.monitor:
            raise Exception("Monitoring is not possible without DBus service!")
        if not args.monitor and not args.quit:
            new_wallpaper()
        
    
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
    parser.add_argument('-t', '--type', metavar='T', type=str, nargs='?', default='local',
                        help='Type of image generator: local or reddit. Default: local')
    parser.add_argument('-s', '--subreddit', metavar='S', type=str, nargs='?', default='earthporn',
                        help='The subreddit for the wallpapers. Default: earthporn')
    parser.add_argument('-d', '--directory', metavar='D', type=str, nargs='?', default='{}/Wallpapers'.format(
        GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES)), help='Directory contains the wallpapers. Default: {}/Wallpapers'.format(
        GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES)))
    parser.add_argument('-o', '--output', metavar='D', type=str, nargs='?', default="{}/Wallpaper.png".format(
        GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES)), help="Target to save the Wallpaper. Default: {}/Wallpaper.png".format(
        GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES)))
    parser.add_argument('-g', '--generate-only', action='store_true', default=False,
                        help='Only generates the image, don\'t set it via gsettings')

    return parser.parse_args()


if __name__ == "__main__":
    main(parse_arguments())
    