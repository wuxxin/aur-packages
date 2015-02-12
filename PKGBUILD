# Maintainer: Sébastien Luttringer
# Maintainer: Daniel Wallace <danielwallace at gtmanfred dot com>
# Contibutor: Christer Edwards <christer.edwards@gmail.com>

pkgbase=salt
pkgname=(salt-zmq salt-raet)
pkgver=2014.7.2
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
             'python2-m2crypto'
             'python2-systemd')
optdepends=('dmidecode: decode SMBIOS/DMI tables'
            'python2-pygit2: gitfs support')
backup=('etc/salt/master'
        'etc/salt/minion')
install=salt.install
conflicts=('salt')
source=("http://pypi.python.org/packages/source/s/salt/salt-$pkgver.tar.gz")
md5sums=('64607e73055626509c59e51fe6feee88')

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
  python2 setup.py --salt-transport=raet install --root="$pkgdir" --optimize=1 \
    --salt-pidfile-dir="/run/salt"

  # default config
  install -Dm644 conf/master "$pkgdir/etc/salt/master"
  install -Dm644 conf/minion "$pkgdir/etc/salt/minion"
  install -d "$pkgdir/etc/salt/master.d/"
  echo 'transport: raet' > "$pkgdir/etc/salt/master.d/transport.conf"

  # systemd services
  for _svc in salt-master.service salt-syndic.service salt-minion.service salt-api.service; do
    install -Dm644 pkg/$_svc "$pkgdir/usr/lib/systemd/system/$_svc"
  done
}

# vim:set ts=2 sw=2 et:
