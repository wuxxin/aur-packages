# Maintainer: wuxxin <wuxxin@gmail.com>

pkgname=coreos-installer
pkgver=0.21.0
pkgrel=1
pkgdesc="Installer for CoreOS disk images"
url="https://github.com/coreos/coreos-installer"
depends=('cargo')
arch=('x86_64')
license=('APACHE')
source=("${pkgname}-${pkgver}.tar.gz::https://github.com/coreos/${pkgname}/archive/refs/tags/v${pkgver}.tar.gz")
sha256sums=('dccda5af41b637c99da7d76a165fed1a770c6bc3f8e23971486c500abe547235')

build() {
  cd "${pkgname}-${pkgver}"
  cargo build --release --locked
}

package() {
  cd "${pkgname}-${pkgver}"
  install -Dm755 "target/release/${pkgname}" "${pkgdir}/usr/bin/${pkgname}"
  install -Dm644 README.md -t "${pkgdir}/usr/share/doc/${pkgname}"
}
