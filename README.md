# WallGen - A random wallpaper generator

## Summary

WallGen is a tool to generate wallpapers matching to your display configuration.

## Restrictions

* Needs a mutter based desktop, for example GNOME,
because WallGen reads the display configurations from mutter's DBus service.

## Requirements

* `python >= 3.6`
* `dbus`
* `glib`
* `imagemagick`
* `wand`, http://wand-py.org/
* `python-pydbus`
* `python-gobject`

## Usage

For a new wallpaper from \$HOME/Pictures/Wallpapers, run:
````
$ wallgen
````

For a new wallpaper from reddit, run:
````
$ wallgen -t reddit
````

For more options, run:
````
$ wallgen -h
````

## Advanced Usage

You can run WallGen as DBus service:
````
$ wallgen --dbus
````

After this every new execution of WallGen will use this service to create new wallpaper.
With WallGen as DBus service you can start it also as monitor for display changes:
````
$ wallgen --monitor
````
Whenever the configuration of your displays changes WallGen generates a matching wallpaper for you.

To stop the DBus service and the monitor, run:
````
$ wallgen --quit
````

