# Maintainer: Jules <jules@agent.local>

pkgname=amux-git
pkgver=0.1.0.r0.g0000000
pkgrel=1
pkgdesc="Multi-session agent orchestrator and control plane (Git version)"
arch=('x86_64' 'aarch64')
url="https://github.com/mixpeek/amux"
license=('MIT')
provides=('amux' 'amux-server')
conflicts=('amux' 'amux-server')
depends=('glibc' 'gcc-libs' 'openssl' 'tmux')
makedepends=('cargo' 'git')
options=('!lto' '!debug')
source=("${pkgname%-git}::git+https://github.com/mixpeek/amux.git"
        "omp-provider.patch")
sha256sums=('SKIP'
            'SKIP')

pkgver() {
    cd "${srcdir}/${pkgname%-git}"
    local _ver=$(grep -m 1 '^version = ' Cargo.toml | cut -d '"' -f 2)
    local _rev=$(git rev-parse --short HEAD)
    local _count=$(git rev-list --count HEAD)
    echo "${_ver}.r${_count}.g${_rev}"
}

prepare() {
    cd "${srcdir}/${pkgname%-git}"
    patch -Np1 -i "${srcdir}/omp-provider.patch"
    export RUSTUP_TOOLCHAIN=stable
    export CARGO_HOME="${srcdir}/.cargo-home"
    cargo fetch --locked --target "$(rustc -vV | sed -n 's/host: //p')"
}

build() {
    cd "${srcdir}/${pkgname%-git}"
    export RUSTUP_TOOLCHAIN=stable
    export CARGO_HOME="${srcdir}/.cargo-home"
    cargo build --release --frozen --workspace
}

package() {
    cd "${srcdir}/${pkgname%-git}"
    install -Dm0755 target/release/amux-server "${pkgdir}/usr/bin/amux-server"
    install -Dm0755 target/release/amux-rs "${pkgdir}/usr/bin/amux-rs"
    install -Dm0755 amux "${pkgdir}/usr/bin/amux"
    install -Dm0755 amux-remote "${pkgdir}/usr/bin/amux-remote"
    install -Dm0644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
    install -Dm0644 README.md "${pkgdir}/usr/share/doc/${pkgname}/README.md"
}
