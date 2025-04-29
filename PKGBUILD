# Maintainer: David Birks <david@birks.dev>

pkgname=goose-desktop
pkgver=1.0.21
pkgrel=1
pkgdesc="An open-source, extensible AI agent that goes beyond code suggestions (with UI)"
arch=("x86_64")
url="https://github.com/block/goose"
license=("Apache-2.0")
depends=(
  "uv"
  "npm"
)
optdepends=()
makedepends=(
  "cargo"
  "nodejs"
  "just"
)
# LTO is broken for dependency ring https://github.com/briansmith/ring/issues/1444
options=("!lto" "!debug")
source=("https://github.com/block/goose/archive/refs/tags/v${pkgver}.tar.gz")
b2sums=('25ef15397a8d5ff377bbdf4b2755570737e98399903a235177030b974e38fbc6623329d9b8e81fb379a88eccd595eb0ed8f6cc02cd956ec4727b249c4e50e581')
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
  
  # Link to local uvx and npx, instead of running the script that installs them with hermit
  rm "$pkgdir/usr/lib/$pkgname/resources/bin/uvx"
  rm "$pkgdir/usr/lib/$pkgname/resources/bin/npx"
  ln -s /usr/bin/uvx "$pkgdir/usr/lib/$pkgname/resources/bin/uvx"
  ln -s /usr/bin/npx "$pkgdir/usr/lib/$pkgname/resources/bin/npx"

  # Install wrapper script, desktop file, and icons
  install -Dm755 "$startdir/goose-desktop.sh" "$pkgdir/usr/bin/$pkgname"
  install -Dm644  ui/desktop/out/Goose-linux-x64/resources/images/icon.png "$pkgdir/usr/share/pixmaps/$pkgname.png"
  install -Dm644 "$startdir/goose-desktop.desktop" "$pkgdir/usr/share/applications/$pkgname.desktop"
}
