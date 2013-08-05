from cmparser import zpool_status,zpool_list_h, zpool_autoreplace, diskmap
from daemon import Daemon
from threading import Timer

class zpoold(Daemon):
    def run(self):
        print 'Data'

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
        #get all disk names
        zconf = []
        disk_names = []
        zconf = []
        disk_names = []
        for name in zname:
            zconf.append(zs.get_zpool_status(name))
            for z in zconf:
                conf = z['config']
                for name in conf:
                    for n in name:
                        disk_names.append(n['name'])
        print disk_names
        full_paths = []
        #get full paths of the disks
        for disk in disk_names:
            full_paths.append(dm.findPathByName(disk))
        print full_paths 
        #get paths and ids:
        ids = []
        for p in [path for path in full_paths if path!='']:
            ids.append(dm.findIdBySymLinks(p))
        print 'ids:'
        print ids
        print '\n'
        print 'disk map:'
        print dm.getdiskMap(disk_names)

if __name__ == '__main__':
    z = zpoold()
    #z.setUp()
    z.run()

