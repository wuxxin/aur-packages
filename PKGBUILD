# Maintainer: wuxxin <wuxxin@gmail.com>
# Contributer: francisco1892 <admin@gnlug.org>
# Contributer: Jingbei Li <i@jingbei.li>
# Contributer: Jose Riha <jose1711 gmail com>

pkgname=python-torchaudio-rocm
_pkgname=audio
pkgver=2.5.1
_sox_ver=14.4.2
pkgrel=1
pkgdesc="Data manipulation and transformation for audio signal processing, powered by PyTorch (with ROCM support)"
arch=('x86_64')
url="https://github.com/pytorch/audio"
license=('BSD')
depends=('python' 'python-pytorch-rocm' 'bzip2' 'xz' 'opencore-amr' 'lame' 'libogg' 'libFLAC.so' 'libvorbis' 'opus' 'opusfile' 'zlib')
optdepends=('python-kaldi-io')
makedepends=('git' 'python-setuptools' 'cmake' 'ninja' 'boost')
conflicts=('python-torchaudio-git' 'python-torchaudio')
provides=('python-torchaudio' "python-torchaudio=${pkgver}")

source=("${url}/archive/refs/tags/v${pkgver}.tar.gz"
	"https://downloads.sourceforge.net/project/sox/sox/$_sox_ver/sox-$_sox_ver.tar.bz2")
sha256sums=('200fbb1234c104a3662b444c0bec2acf4049c4b2113a73c0dc5f4e672cc2a4cc'
	'81a6956d4330e75b5827316e44ae381e6f1e8928003c6aa45896da9041ea149c')

# architecture list taken from corresponding pytorch package: arch:python-pytorch@2.5.1-3
_PYTORCH_ROCM_ARCH="gfx900;gfx906:xnack-;gfx908:xnack-;gfx90a:xnack+;gfx90a:xnack-;gfx940;gfx941;gfx942;gfx1010;gfx1012;gfx1030;gfx1100;gfx1101;gfx1102"

prepare() {
	cd "$srcdir/${_pkgname}-${pkgver}"
	git submodule init
}

build() {
	cd "$srcdir/${_pkgname}-${pkgver}"

    if test -n "$GPU_TARGETS"; then _PYTORCH_ROCM_ARCH="$GPU_TARGETS"; fi
    if test -n "$AMDGPU_TARGETS"; then _PYTORCH_ROCM_ARCH="$AMDGPU_TARGETS"; fi
    if test -n "$PYTORCH_ROCM_ARCH"; then _PYTORCH_ROCM_ARCH="$PYTORCH_ROCM_ARCH"; fi
    export PYTORCH_ROCM_ARCH="${_PYTORCH_ROCM_ARCH}"
    echo "building for PYTORCH_ROCM_ARCH=$PYTORCH_ROCM_ARCH"

    # if ROCM_HOME is not set, hardcode ROCM_HOME, ROCM_PATH, HIP_ROOT_DIR to /opt/rocm
    export ROCM_HOME="${ROCM_HOME:-/opt/rocm}"
    export ROCM_PATH="$ROCM_HOME"
    export HIP_ROOT_DIR="$ROCM_HOME"

    BUILD_SOX=1 USE_ROCM=1 python setup.py build
}

package() {
	cd "$srcdir/${_pkgname}-${pkgver}"
	BUILD_SOX=1 USE_ROCM=1 python setup.py install --root="$pkgdir"/ --optimize=1
	install -Dm644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}
