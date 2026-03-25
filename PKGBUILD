# Maintainer: Marcel Hoppe <hoppe.marcel@gmail.com>

pkgname=wallgen-git
pkgver=26.3.1
pkgrel=1
pkgdesc='WallGen is a tool to generate wallpapers matching for your display configuration.'
arch=('any')
source=("git+https://github.com/hobbypunk90/WallGen.git")
sha256sums=(SKIP)
license=('GPL')
depends=('python' 'python-wand' 'python-pydbus' 'python-gobject' 'python-yaml' 'imagemagick')
makedepends=('git' 'python-build' 'python-installer' 'python-wheel')
provides=('wallgen')
conflicts=('wallgen')

pkgver() {
  cd "WallGen"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

build() {
  cd "WallGen"
  /usr/bin/python -m build --wheel --no-isolation
}

package() {
  cd "WallGen"
  /usr/bin/python -m installer --destdir="$pkgdir" dist/*.whl

  DESTSYSTEMD="$pkgdir/usr/lib/systemd/user"
  install -Dm644 "systemd/wallgen.service" "$DESTSYSTEMD/wallgen.service"
  install -Dm644 "systemd/wallgen.timer" "$DESTSYSTEMD/wallgen.timer"
  install -Dm644 "systemd/wallgen-dbus.service" "$DESTSYSTEMD/wallgen-dbus.service"
  install -Dm644 "systemd/wallgen-monitor.service" "$DESTSYSTEMD/wallgen-monitor.service"
}
