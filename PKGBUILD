# Maintainer: David Birks <david@birks.dev>

pkgname=goose-desktop
pkgver=1.0.35
pkgrel=2
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
source=(
  "https://github.com/block/goose/archive/refs/tags/v${pkgver}.tar.gz"
  "auto-hide-menu-bar.patch"
)
b2sums=('4a65ce80da087ffcf23c236677c1385ab688375ae2204459f362c560114a76366dd63ab26c04db87376517b7479d3e515367affbf382696bb7dd5da6c46bc16e'
        '94d5a2add73bcde850f5c0555039d71b63611e54dc896ab8b5c12165884ad4126e3298c6542a10d82ef9b84f6b191468c6ba4a7843a854c560facd3591b5bdc5')
conflicts=(
  "codename-goose"
  "codename-goose-bin"
)

prepare() {
  cd goose-$pkgver

  # Apply patches
  patch -Np1 -i "$srcdir/auto-hide-menu-bar.patch"
}

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

  # To fix error from Forge:
  # > Cannot find module @rollup/rollup-linux-x64-gnu.
  npm i @rollup/rollup-linux-x64-gnu@4.43.0

  # To fix error from Forge:
  # > Error: The package "@esbuild/linux-x64" could not be found, and is needed by esbuild.
  npm i @esbuild/linux-x64@0.25.5

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
