from cmparser import zpool_status,zpool_list_h, zpool_autoreplace, diskmap
from notifier import mail_notification
from daemon import Daemon
import time
from config import config
from threading import Timer


class zpoold(Daemon):
    def run(self):
        time.sleep(config['daemon']['daemon_freq_s'])
        self.setUp()
        self.sent = 'not_sent'

    def setUp(self):
        zl = zpool_list_h()
        zs = zpool_status()
        dm = diskmap()
        #get full list of avialable zpool names
        zname = [zname['name'] for zname in zl.get_zpool_list_h()]
        #get config
        #print zname
        #print '\n'
        #get all disk names
        zconf = []
        disk_names = []
        for name in zname:
            zconf.append(zs.get_zpool_status(name))
            for z in zconf:
                conf = z['config']
                for name in conf:
                    for n in name:
                        disk_names.append(n['name'])
                        if n['state'] != 'ONLINE':
                            if not self.sent == 'waiting' :
                                mail = mail_notification()
                                mail.sendNotification(message = str(disk_names), subj=n['state'])
                                self.sent = True
                            else:
                                try:
                                    t = Timer(int(config['mail_conf']['mail_frequency_min']) * 60, mail.sendNotification, [str(disk_names), n['state']])
                                    t.start()
                                    self.sent = 'waiting'
                                except Exception, e:
                                    print "Now waiting timer Error: %e" % e
        #print disk_names
        full_paths = []
        #get full paths of the disks
        for disk in disk_names:
            full_paths.append(dm.findPathByName(disk))
        #print full_paths
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

