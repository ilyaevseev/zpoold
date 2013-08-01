from cmparser import zpool_status,zpool_list_h, zpool_autoreplace
from daemon import Daemon
from threading import Timer

class zpoold():
    def setUp(self):
        zpool_list = zpool_list_h()
        zpool_stat = zpool_status()
        zpool_auto = zpool_autoreplace()
        print 'starting:\n'
        out = zpool_list.get_zpool_list_h()
        print 'list of zpool:\n'
        for o['name'] in out:
            print o['name']
        print 'zpool list -H %s\n' % (o['name'] for o in out)
        for o['name'] in out:
            print zpool_stat.get_zpool_status(o['name'])
        print 'get autoreplace:\n'
        print zpool_auto.get_autoreplace()

z = zpoold()
z.setUp()
