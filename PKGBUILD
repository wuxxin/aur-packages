# Maintainer: David Birks <david@birks.dev>

pkgname=goose-desktop
pkgver=1.0.24
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
  "oniguruma"
)
# LTO is broken for dependency ring https://github.com/briansmith/ring/issues/1444
options=("!lto" "!debug")
source=("https://github.com/block/goose/archive/refs/tags/v${pkgver}.tar.gz")
b2sums=('fbdb973ad14d9923fc5ea390e94de54e8e06bcedfdc6d115d08229664e10c365126988f7087de6407ca114b994d40a3f16ce250f958f84d6e2fc7dc726a454e9')
conflicts=(
  "codename-goose"
  "codename-goose-bin"
)

build() {
  cd goose-$pkgver

  # Use the prebuilt oniguruma for now
  # https://github.com/block/goose/issues/2572
  export RUSTONIG_SYSTEM_LIBONIG=1

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
