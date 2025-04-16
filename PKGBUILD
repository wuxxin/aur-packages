# Maintainer: David Birks <david@birks.dev>

pkgname=goose-desktop
pkgver=1.0.18
pkgrel=2
pkgdesc="An open-source, extensible AI agent that goes beyond code suggestions (with UI)"
arch=("x86_64")
url="https://github.com/block/goose"
license=("Apache-2.0")
depends=()
optdepends=()
makedepends=(
  "cargo"
  "nodejs"
  "just"
)
# LTO is broken for dependency ring https://github.com/briansmith/ring/issues/1444
options=("!lto" "!debug")
source=("https://github.com/block/goose/archive/refs/tags/v${pkgver}.tar.gz")
b2sums=("c1f0e98dc30232aee7e61be0ba483bca35daef6073358358343aa2ffda780829509c884c4b64aefc9ca4d6d06e00ab431ff3fc387daa6a22c99abc1238c099f7")
conflicts=(
  "codename-goose"
  "codename-goose-bin"
)

build() {
  cd goose-$pkgver

  # Build the command-line binary
  just release-binary

  cd ui/desktop
  # Install dependencies, ignoring the prepare script which tries to run husky
  npm ci --ignore-scripts

  # Build the Electron app
  npx electron-forge package
}

package() {
  cd goose-$pkgver
  
  # Install command-line binary
  install -Dm755 "target/release/goose" "$pkgdir/usr/bin/goose"
  
  # Install the Electron app
  mkdir -p "$pkgdir/usr/lib/$pkgname"
  cp -r "ui/desktop/out/Goose-linux-x64/"* "$pkgdir/usr/lib/$pkgname/"
  
  # Install wrapper script, desktop file, and icons
  install -Dm755 "$startdir/goose-desktop.sh" "$pkgdir/usr/bin/$pkgname"
  install -Dm644  ui/desktop/out/Goose-linux-x64/resources/images/icon.png "$pkgdir/usr/share/pixmaps/$pkgname.png"
  install -Dm644 "$startdir/goose-desktop.desktop" "$pkgdir/usr/share/applications/$pkgname.desktop"
}
