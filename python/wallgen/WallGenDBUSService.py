import os

from pydbus import SessionBus
from pydbus.generic import signal

from wand.image import Image


from .from_reddit import RedditGenerator
from .from_local import LocalGenerator
from wallgen import Config, __util__


class WallGenDBUSService(object):
    dbus = """
    <node>
    	<interface name="de.thm.mni.mhpp11.WallGen">
    		<signal name="Closed" />
    		<method name="NewWallpaper" />
    		<method name="Close" />
    	</interface>
    </node>
    """
    Closed = signal()
    
    def __init__(self, loop):
        self.config = Config()
        self.loop = loop
    
    def NewWallpaper(self, _=None):
        builder = None
        print("Create a new Wallpaper...")
        bus = SessionBus()

        if self.config.type == 'reddit':
            generator = RedditGenerator(self.config.subreddit)
        else:
            generator = LocalGenerator(self.config.directory)

        if self.config.is_gnome():
            builder = GnomeWallpaperBuilder(bus, self.config)
        elif self.config.is_kde():
            builder = KDEWallpaperBuilder(bus, self.config)

        builder.build(generator)


    def Close(self):
        self.Closed()
        self.loop.quit()

class GnomeWallpaperBuilder:

    def __init__(self, bus, config):
        self.dc = bus.get('org.gnome.Mutter.DisplayConfig')
        self.config = config

    def build(self, generator):
        active_monitors = []
        for monitor in self.dc.GetResources()[1]:
            if monitor[6] > -1:
                active_monitors.append(monitor)
        (max_width, max_height) = self._get_maximum_resolution(active_monitors)
        with Image(width=max_width, height=max_height) as wallpaper:
            for monitor in active_monitors:
                image = generator.get_image(width=monitor[4], height=monitor[5])
                wallpaper.composite(image, left=monitor[2], top=monitor[3])
                with wallpaper.convert('png') as converted:
                    self._save(converted, self.config)

    def _save(self, image, config):
        output = '{}/Wallpaper.png'.format(config.output)
        __util__.save(image, output)
        if not config.generate_only:
            from gi.repository import Gio
            settings_background = Gio.Settings("org.gnome.desktop.background")
            settings_screensaver = Gio.Settings("org.gnome.desktop.screensaver")
            file = "file://{}".format(output)
            if (not config.disable_background) and settings_background.get_string("picture-uri") != file:
                print("set!")
                settings_background.set_string("picture-uri", file)
            if (not config.disable_lockscreen) and settings_screensaver.get_string("picture-uri") != file:
                print("set!")
                settings_screensaver.set_string("picture-uri", file)


    def _get_maximum_resolution(self, monitor_list):
        max_resolution = None
        for monitor in monitor_list:
            if max_resolution == None:
                max_resolution = (monitor[2] + monitor[4], monitor[3] + monitor[5])
            else:
                width = monitor[2] + monitor[4]
                if width >= max_resolution[0]:
                    max_resolution = (width, max_resolution[1])

                height = monitor[3] + monitor[5]
                if height >= max_resolution[1]:
                    max_resolution = (max_resolution[0], height)
        return max_resolution


class KDEWallpaperBuilder:

    def __init__(self, bus, config):
        self.kscreen = bus.get('org.kde.KScreen', object_path='/backend')
        self.plasma_shell = bus.get('org.kde.plasmashell', object_path='/PlasmaShell')
        self.config = config

    def build(self, generator):
        active_monitors = []
        test = self.kscreen.getConfig()
        for monitor in test['outputs']:
            if monitor['connected'] and monitor['enabled']:
                active_monitors.append(monitor)

        for monitor in active_monitors:
            image = generator.get_image(width=int(monitor['size']['width']), height=int(monitor['size']['height']))
            with image.convert('png') as converted:
                self._save(converted, self.config, monitor, len(active_monitors))

    def _save(self, image, config, monitor, count):
        output = "{}/Wallpaper_{}.png".format(config.output, monitor['name'])
        tmp_output = "{}/Wallpaper_{}_tmp.png".format(config.output, monitor['name'])
        __util__.save(image, tmp_output)
        __util__.save(image, output)
        if not config.generate_only:

            if (not config.disable_background):
                print("set {}!".format(monitor['name']))

                script = """
                    var Desktops = desktops()
                    var desktop = undefined
                    var screen_id = undefined
                    for(i = 0; i < {}; i++) {{
                        s = screenGeometry(i)
                        if(s['x'] == {} && s['y'] == {}) {{
                            screen_id = i
                            break
                        }}
                    }}
                    if(screen_id !== undefined)
                        desktop = desktopForScreen(screen_id)
                    if(desktop) {{
                        desktop.wallpaperPlugin = "org.kde.image"
                        desktop.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General")
        
                        desktop.writeConfig("Image", "{}")
                        desktop.writeConfig("Image", "{}")
                    }}
                    """.format(count+10, int(monitor['pos']['x']), int(monitor['pos']['y']), "file://{}".format(tmp_output), "file://{}".format(output))
                self.plasma_shell.evaluateScript(script)
        os.remove(tmp_output)