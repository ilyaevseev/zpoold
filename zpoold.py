from cmparser import zpool_status,zpool_list_h, zpool_autoreplace, diskmap
from notifier import mail_notification
from daemon import Daemon
from threading import Timer, Event, Thread
import time
from config import config

class Timer(Thread):

    def __init__(self, number_of_sec = 30):
        self.number_of_sec = number_of_sec
        Thread.__init__(self)
        self.event = Event()
    def run(self):
        while not self.event.is_set():
            #TODO the job
            self.event.wait(self.number_of_sec)
    def stop(self):
        self.event.set()

class zpoold(Daemon):
    def run(self):
        while(True):
           time.sleep(100)
           self.setUp()

    def setUp(self):
        zl = zpool_list_h()
        zs = zpool_status()
        mail = mail_notification()
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
                            mail.sendNotification(message = str(disk_names), subj=n['state'])
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
        #print 'ids:'
        #print ids
        #print '\n'
        #print 'disk map:'
        #print dm.getdiskMap(disk_names)

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

