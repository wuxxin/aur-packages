# Maintainer: Cody Wyatt Neiman (xangelix) <neiman@cody.to>

_name=bitsandbytes
pkgname=python-$_name-rocm-git
pkgdesc="Lightweight wrapper around CUDA custom functions, in particular 8-bit optimizers, matrix multiplication (LLM.int8()), and quantization functions (official AMD ROCm fork)"
license=("MIT")
url="https://github.com/ROCm/$_name"
pkgver=0.41.0.r312.g5bada9b
pkgrel=2
arch=("x86_64")
makedepends=("make" "cmake")
depends=("hipblaslt" "hiprand" "hipsparse" "hipcub" "rocthrust" "python-setuptools" "python-pytest" "python-einops" "python-wheel" "python-scipy" "python-lion-pytorch" "python-pandas" "python-matplotlib")
provides=("python-$_name")
conflicts=("python-$_name-git" "python-$_name-cuda121")
source=("$pkgname::git+$url")
sha512sums=("SKIP")


pkgver() {
  cd $pkgname

  ( set -o pipefail
    # cutting off 'v' prefix that presents in the git tag
    git describe --tags | sed 's/^v//;s/\([^-]*-g\)/r\1/;s/-/./g' ||
    printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
  )
}


build() {
  cd $pkgname

  cmake -DCOMPUTE_BACKEND=hip -S .
  make
  python -m build --wheel --no-isolation
}


package() {
  # Install license
  install -Dm644 $pkgname/LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"

  # Install the python wheel
  python -m installer --destdir="$pkgdir" $pkgname/dist/*.whl
}
