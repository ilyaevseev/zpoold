from cmparser import zpool_status,zpool_list_h, zpool_autoreplace, diskmap
from daemon import Daemon
from threading import Timer

class zpoold(object):
    def setUp(self):
        zl = zpool_list_h()
        za = zpool_autoreplace()
        zs = zpool_status()
        dm = diskmap()
        #get full list of avialable zpool names
        zname = [zname['name'] for zname in zl.get_zpool_list_h()]
        #get config
        print zname
        print '\n'
        zconf = []
        for name in zname:
            zconf.append(zs.get_zpool_status(name))
        print zconf
        conf = zconf['config']
        names = []
        for conf in zconf['name']:
            names.append(conf)
        print 'names:'
        print names
        full_paths = []
        for name in names:
            full_paths.append(dm.findPathByName(name))
        print 'Full paths:'
        print full_paths
        ids = []
        for path in full_paths:
            ids.append(dm.findIdBySymLinks(path))
        print 'ids:'
        print ids
        print '\n'
        print 'disk map:'
        print dm.getdiskMap(names)
        


if __name__ == '__main__':
    z = zpoold()
    z.setUp()

