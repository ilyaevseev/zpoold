from cmparser import zpool_status,zpool_list_h, zpool_autoreplace, diskmap
from notifier import mail_notification
from daemon import Daemon
import time
from config import config
import logging

class zpoold(Daemon):
    def run(self):
        self.setUp()

    def setUp(self):
        logging.basicConfig(filename='log.txt', level=logging.DEBUG)
        zl = zpool_list_h()
        zs = zpool_status()
        dm = diskmap()
        self.id_unv = ''

        zname = [zname['name'] for zname in zl.get_zpool_list_h()]
        logging.debug('get full list of avialable zpool names')
        logging.debug(zname)
        zconf = []
        disk_names = []
        for name in zname:
            zconf.append(zs.get_zpool_status(name))
            logging.debug('zpool status')
            logging.debug(zs.get_zpool_status(name))
            for z in zconf:
                conf = z['config']
                logging.debug('pool config')
                logging.debug(conf)
                for name in conf:
                    logging.debug('name')
                    logging.debug(name)
                    for n in name:
                        disk_names.append(n['name'])
                        logging.debug('disk names')
                        logging.debug(disk_names)
                        if n['state'] == 'UNAVAIL':
                            mail = mail_notification()
                            mail.sendNotification(message = str(disk_names), subj=n['state'])
                            oldpath = dm.findIdBySymLinks((dm.findPathByName(n['name'])))['by-path']
                            logging.debug('old path:')
                            logging.debug(oldpath)
                            if self.id_unv == '':
                                self.id_unv = dm.findIdBySymLinks((dm.findPathByName(n['name'])))['by-id']
                                logging.debug('id unv:')
                                logging.debug(self.id_unv)
                            elif self.id_unv != dm.findIdBySymLinks((dm.findPathByName(n['name'])))['by-id']:
                                logging.debug('Startinf replacing:')
                                zs.replaceDisk(zname, oldpath)
        full_paths = []
        logging.debug('get full paths of the disks')
        for disk in disk_names:
            full_paths.append(dm.findPathByName(disk))
        logging.debug(full_paths)
        ids = []
        for p in [path for path in full_paths if path!='']:
            ids.append(dm.findIdBySymLinks(p))
        logging.debug('ids:')
        logging.debug(ids)
        logging.debug('disk map:')
        logging.debug(dm.getdiskMap(disk_names))

if __name__ == '__main__':
    import sys
    z = zpoold(config['daemon']['pid_path'])
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            z.start()
        elif 'stop' == sys.argv[1]:
            z.stop()
        elif 'restart' == sys.argv[1]:
            z.restart()
        else:
            print "Unknown command"
            sys.exit(2)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

