# Maintainer: Sébastien Luttringer
# Maintainer: Daniel Wallace <danielwallace at gtmanfred dot com>
# Contibutor: Christer Edwards <christer.edwards@gmail.com>

pkgbase=salt
pkgname=(salt-zmq salt-raet)
pkgver=2014.7.0
pkgrel=1
pkgdesc='Central system and configuration manager'
arch=('any')
url='http://saltstack.org/'
license=('Apache')
makedepends=('python2'
             'python2-jinja'
             'python2-msgpack'
             'python2-yaml'
             'python2-markupsafe'
             'python2-requests'
             'python2-libnacl'
             'python2-ioflo'
             'python2-raet'
             'python2-pyzmq'
             'python2-crypto'
             'python2-m2crypto')
optdepends=('dmidecode: decode SMBIOS/DMI tables'
            'python2-pygit2: gitfs support')
backup=('etc/salt/master'
        'etc/salt/minion')
install=salt.install
conflicts=('salt')
source=("http://pypi.python.org/packages/source/s/salt/salt-$pkgver.tar.gz")
md5sums=('3bbb6194f9146a5efad8963c9340d4cd')

package_salt-zmq() {
  cd $pkgbase-$pkgver
  provides=('salt' 'salt-api')
  replaces=('salt<=2014.1.13' 'salt-api<2014.7')
  depends=('python2-jinja'
           'python2-msgpack'
           'python2-yaml'
           'python2-markupsafe'
           'python2-requests'
           'python2-pyzmq'
           'python2-crypto'
           'python2-m2crypto'
           'python2-systemd')
  python2 setup.py clean
  python2 setup.py install --root="$pkgdir" --optimize=1 \
    --salt-pidfile-dir="/run/salt"

  # default config
  install -Dm644 conf/master "$pkgdir/etc/salt/master"
  install -Dm644 conf/minion "$pkgdir/etc/salt/minion"

  # systemd services
  for _svc in salt-master.service salt-syndic.service salt-minion.service salt-api.service; do
    install -Dm644 pkg/$_svc "$pkgdir/usr/lib/systemd/system/$_svc"
  done
}

package_salt-raet() {
  cd $pkgbase-$pkgver
  provides=('salt' 'salt-api')
  depends=('python2-jinja'
           'python2-msgpack'
           'python2-yaml'
           'python2-markupsafe'
           'python2-requests'
           'python2-libnacl'
           'python2-ioflo'
           'python2-raet'
           'python2-systemd')
  python2 setup.py clean
  python2 setup.py install --root="$pkgdir" --optimize=1 \
    --salt-pidfile-dir="/run/salt" --salt-transport=raet

  # default config
  install -Dm644 conf/master "$pkgdir/etc/salt/master"
  install -Dm644 conf/minion "$pkgdir/etc/salt/minion"

  # systemd services
  for _svc in salt-master.service salt-syndic.service salt-minion.service salt-api.service; do
    install -Dm644 pkg/$_svc "$pkgdir/usr/lib/systemd/system/$_svc"
  done
}

# vim:set ts=2 sw=2 et:
