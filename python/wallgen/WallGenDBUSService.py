from pydbus import SessionBus
from pydbus.generic import signal

from wand.image import Image

from wallgen import from_reddit as reddit_generator
from wallgen import from_local as local_generator
from wallgen import __util__


class WallGenDBUSService(object):
    dbus = """
    <node>
    	<interface name="de.thm.mni.mhpp11.WallGen">
    		<signal name="Closed" />
    		<method name="NewWallpaper">
    			<arg direction="in" type="s" name="type"/>
    			<arg direction="in" type="s" name="subredit"/>
    			<arg direction="in" type="s" name="directory"/>
    			<arg direction="in" type="s" name="output"/>
    			<arg direction="in" type="b" name="generate_only"/>
    		</method>
    		<method name="Close" />
    	</interface>
    </node>
    """
    Closed = signal()
    
    def __init__(self, loop):
        self.loop = loop
    
    def NewWallpaper(self, type, subreddit, directory, output, generate_only):
        print("Create a new Wallpaper...")
        bus = SessionBus()
        dc = bus.get('org.gnome.Mutter.DisplayConfig')
        
        if type == 'reddit':
            generator = reddit_generator
            option = subreddit
        else:
            generator = local_generator
            option = directory
        
        active_monitors = []
        for monitor in dc.GetResources()[1]:
            if monitor[6] > -1:
                active_monitors.append(monitor)
        (max_width, max_height) = get_maximum_resolution(active_monitors)
        with Image(width=max_width, height=max_height) as wallpaper:
            for monitor in active_monitors:
                image = generator.get_image(option, width=monitor[4], height=monitor[5])
                wallpaper.composite(image, left=monitor[2], top=monitor[3])
                with wallpaper.convert('png') as converted:
                    save(converted, output, generate_only)
    
    def Close(self):
        self.Closed()
        self.loop.quit()


def save(image, file, generate_only):
    __util__.save(image, file)
    if not generate_only:
        from gi.repository import Gio
        settings_background = Gio.Settings("org.gnome.desktop.background")
        settings_screensaver = Gio.Settings("org.gnome.desktop.screensaver")
        file = "file://{}".format(file)
        if settings_background.get_string("picture-uri") != file:
            print("set!")
            settings_background.set_string("picture-uri", file)
        if settings_screensaver.get_string("picture-uri") != file:
            print("set!")
            settings_screensaver.set_string("picture-uri", file)


def get_maximum_resolution(monitor_list):
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