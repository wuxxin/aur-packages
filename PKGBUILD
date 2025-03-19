# Maintainer: Wuxxin <wuxxin@gmail.com>
# Contributor: Johannes Löthberg <johannes@kyriasis.com>
# Contributor: Morten Linderud <foxboron@archlinux.org>
# Contributor: Sébastien Luttringer
# Contributor: Daniel Wallace <danielwallace at gtmanfred dot com>
# Contributor: Christer Edwards <christer.edwards@gmail.com>
# Contributor: zer0def <zer0def@github>

pkgname=salt
pkgver=3007.1
pkgrel=6
pkgdesc='Portable, distributed, remote execution and configuration management system'
arch=('any')
url='https://saltproject.io/'
license=('Apache')
replaces=('salt-zmq' 'salt-raet')
conflicts=('salt-zmq' 'salt-raet')
# dependencies: base, crypto, zeromq; ignore contextvars, timelib; extra: systemd
depends=(
  'python-jinja'
  'python-jmespath'
  'python-msgpack'
  'python-yaml'
  'python-markupsafe'
  'python-networkx'
  'python-requests'
  'python-certifi'
  'python-distro'
  'python-psutil'
  'python-packaging'
  'python-looseversion'
  'python-tornado'
  'python-aiohttp'
  'python-urllib3'
  'python-croniter'
  'python-setproctitle'
  'python-pyopenssl'
  'python-dateutil'
  'python-gnupg'
  'python-cherrypy'
  'python-importlib-metadata'
  'python-cryptography'
  'python-pycryptodomex'
  'python-pyzmq'
  'python-systemd'
)

makedepends=(
  'python-setuptools'
)
optdepends=(
  'dmidecode: decode SMBIOS/DMI tables'
  'python-pygit2: gitfs support'
)
#checkdepends=('python-pytest' 'python-psutil')
backup=(
  'etc/logrotate.d/salt'
  'etc/salt/master'
  'etc/salt/minion'
)
install=salt.install
source=(
  "https://pypi.io/packages/source/s/salt/salt-$pkgver.tar.gz"
  salt.logrotate
  contextvars.patch
  rpmvercmp.patch
  urllib.patch
  has_crypt.patch
  salt-call
)
sha256sums=(
  'b933ac4cb3e4b1118b46dada55c9cc6bdc6f0f94b4c92877aec44b25c6a28c9a'
  'abecc3c1be124c4afffaaeb3ba32b60dfee8ba6dc32189edfa2ad154ecb7a215'
  'SKIP'
  'SKIP'
  'SKIP'
  'SKIP'
  'SKIP'
)

prepare() {
  cd "${srcdir}/${pkgname}-${pkgver}"
  for i in contextvars rpmvercmp urllib has_crypt; do
    patch -N -p1 -i "${srcdir}/${i}.patch"
  done
}

build() {
  cd "${srcdir}/${pkgname}-${pkgver}"
  python setup.py build
}

package() {
  install -Dm644 salt.logrotate "$pkgdir"/etc/logrotate.d/salt

  cd "${srcdir}/${pkgname}-${pkgver}"

  python setup.py --salt-pidfile-dir="/run/salt" install --root="$pkgdir" --optimize=1 --skip-build
  # workaround KeyError: 'config.option'
  cp ${srcdir}/salt-call ${pkgdir}/usr/bin/salt-call

  # default config
  install -v -Dm644 conf/master "$pkgdir/etc/salt/master"
  install -v -Dm644 conf/minion "$pkgdir/etc/salt/minion"

  # systemd services
  for _svc in salt-master.service salt-syndic.service salt-minion.service salt-api.service; do
    install -v -Dm644 pkg/common/$_svc "$pkgdir/usr/lib/systemd/system/$_svc"
  done
  install -v -Dm644 pkg/common/salt.bash "$pkgdir/usr/share/bash-completion/completions/salt"
  install -v -Dm644 pkg/common/salt.zsh "$pkgdir/usr/share/zsh/site-functions/_salt"
  install -v -Dm644 -t "$pkgdir/usr/share/fish/vendor_completions.d" pkg/common/fish-completions/*
}

# vim:set ts=2 sw=2 et:
