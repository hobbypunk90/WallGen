# Maintainer: Marcel Hoppe <hoppe.marcel@gmail.com>

pkgname=python-wallgen
pkgbase=${pkgname}
pkgver=0.2.1
pkgrel=1
_tag=${pkgver}
_name=${pkgname#python-}
pkgdesc='WallGen is a tool to generate wallpapers matching for your display configuration.'
arch=('any')
source=("git+https://github.com/hobbypunk90/WallGen.git#tag=${_tag}")
sha256sums=(SKIP)
license=('GPL')
depends=('python>=3.10' 'python-yaml' 'python-pydbus' 'python-gobject' 'imagemagick' 'python-wand')
makedepends=('python-build' 'python-installer' 'python-wheel')

build() {
  cd "$srcdir/WallGen"
  python -m build --wheel --no-isolation
}

package() {
  cd "$srcdir/WallGen"
  python -m installer --destdir="$pkgdir" dist/*.whl
  DESTSYSTEMD="$pkgdir/etc/systemd/user"
  install -Dm644 "systemd/wallgen.service" "$DESTSYSTEMD/wallgen.service"
  install -Dm644 "systemd/wallgen.timer" "$DESTSYSTEMD/wallgen.timer"
  install -Dm644 "systemd/wallgen-dbus.service" "$DESTSYSTEMD/wallgen-dbus.service"
  install -Dm644 "systemd/wallgen-monitor.service" "$DESTSYSTEMD/wallgen-monitor.service"
}