# Maintainer: Sébastien Luttringer
# Maintainer: Daniel Wallace <danielwallace at gtmanfred dot com>
# Contibutor: Christer Edwards <christer.edwards@gmail.com>

pkgname=salt
pkgver=2014.1.11
pkgrel=1
pkgdesc='Central system and configuration manager'
arch=('any')
url='http://saltstack.org/'
license=('Apache')
depends=('python2'
         'python2-crypto'
         'python2-jinja'
         'python2-m2crypto'
         'python2-msgpack'
         'python2-psutil'
         'python2-pyzmq'
         'python2-systemd'
         'python2-requests'
         'python2-yaml'
         'apache-libcloud'
         'sshpass')
optdepends=('dmidecode: decode SMBIOS/DMI tables'
            'python2-pygit2: gitfs support')
backup=('etc/salt/master'
        'etc/salt/minion')
install=salt.install
source=("http://pypi.python.org/packages/source/s/salt/salt-$pkgver.tar.gz")
md5sums=('784d7a9034c88ea62388238d7e24912d')

package() {
  cd $pkgname-$pkgver
  python2 setup.py install --root="$pkgdir" --optimize=1 \
    --salt-pidfile-dir="/run/salt"

  # default config
  install -Dm644 conf/master "$pkgdir/etc/salt/master"
  install -Dm644 conf/minion "$pkgdir/etc/salt/minion"

  # systemd services
  for _svc in salt-master.service salt-syndic.service salt-minion.service; do
    install -Dm644 pkg/$_svc "$pkgdir/usr/lib/systemd/system/$_svc"
  done
}

# vim:set ts=2 sw=2 et:
