'''
base class for stdout parse
'''
import subprocess
import platform
from sys import exit
from collections import OrderedDict as ordereddict

class cmparser(object):
    def isLinux(self):
        if not platform.system().lower().startswith('linux'):
            raise Exception('is not Linux platform, this daemon for Linux only')

    def execute(self, commands):
        self.isLinux()
        p = subprocess.Popen(commands, stdout=subprocess.PIPE)
        return p.communicate()

class zpool_list_h(cmparser):
    def __init__(self):
        self.structure_dict = ordereddict([
                    ('name',''),
                    ('full_size',''),
                    ('m_size',''),
                    ('full_size2',''),
                    ('usage',''),
                    ('speed',''),
                    ('status',''),
                    ('other_part',''),
                    ])
        self.list_of_structures = []

    def get_zpool_list_h(self, commands = ['zpool', 'list', '-H']):
        out, error = self.execute(commands)
        if error != None:
            raise Exception('There is no zpool avialable, {Error %s}' % error)
            exit(1)
        else:
            for line in [i for i in out.splitlines() if i!='']:
                for key, word in zip(self.structure_dict.keys(),line.split(None)):
                    self.structure_dict[key] = word
                self.list_of_structures.append(self.structure_dict.copy())
            return self.list_of_structures

class zpool_autoreplace(cmparser):
    def __init__(self):
        self.structure_dict = ordereddict([
                    ('name',''),
                    ('property',''),
                    ('value',''),
                    ('source',''),
                    ])
        self.list_of_structures = []
    def get_autoreplace(self, commands = ['zpool','get','autoreplace']):
        out, error = self.execute(commands)
        if error != None:
            raise Exception('There is no zpool avialable, {Error %s}' % error)
            exit(1)
        else:
            for line in [i for i in out.splitlines() if i!=''][1:]:
                for key, word in zip(self.structure_dict.keys(),line.split(None)[:4]):
                    self.structure_dict[key] = word
                self.list_of_structures.append(self.structure_dict.copy())
            return self.list_of_structures

class zpool_status(cmparser):
    def __init__(self):
        self.config = ordereddict([
            ('name',''),
            ('state',''),
            ('read',''),
            ('write',''),
            ('cksum',''),
            ])
        self.structure_dict = ordereddict([
            ('pool',''),
            ('state',''),
            ('scan',''),
            ('action',''),
            ('see',''),
            ('scrub',''),
            ('status',''),
            ('config', []),
            ('errors', []),
            ])

    def isHealthy(self, commands = ['zpool', 'status', '-x']):
        out, error = self.execute(commands)
        if error != None:
            raise Exception('There is no zpool avialable, {Error %s}' % error)
            exit(1)
        else:
            if out.strip().find('all pools are healthy') != -1:
                return True
            else:
                return False

    def replaceDisk(self, zpool_name, new_disk, commands = ['zpool','replace',\
            'zpool_name', 'new_disk']):
        commands[2] = zpool_name
        commands[3] = new_disk
        out, error = self.execute(commands)
        if error != None:
            raise Exception('There is no zpool avialable, {Error %s}' % error)
            exit(1)
        else:
            return 0

    def get_zpool_status(self, zpool_name, commands = ['zpool','status', 'zpool_name', '-v']):
        commands[2] = zpool_name
        out, error = self.execute(commands)
        if error != None:
            raise Exception('There is no zpool avialable, {Error %s}' % error)
            exit(1)
        else:
            stopwords = self.structure_dict.keys()
            prev_word = ''; i, g = 0,0
            config = []; error = []
            for line in out.splitlines():
                row = line.split(None)
                if len(row) > 0:
                    if row[0][:-1] in stopwords:
                        if row[0][:-1] == 'pool':
                            self.structure_dict['pool'] = row[1:]
                            prev_word = 'pool'
                        elif row[0][:-1] == 'state':
                            self.structure_dict['state'] = row[1:]
                            prev_word = 'state'
                        elif row[0][:-1] == 'scan':
                            self.structure_dict['scan'] = row[1:]
                            prev_word = 'scan'
                        elif row[0][:-1] == 'errors':
                            self.structure_dict['errors'] = row[1:]
                            prev_word = 'errors'
                        elif row[0][:-1] == 'config':
                            prev_word = 'config'
                    else:
                        if prev_word == 'config':
                            i+=1
                            if i > 1:
                                for word, key in zip(row[:5], self.config.keys()):
                                    self.config[key] = word
                                config.append(self.config.copy())
                        if prev_word == 'errors':
                            error.append(row)
            self.structure_dict['errors'].append(error)
            self.structure_dict['config'].append(config)
            i,g = 0,0
            return self.structure_dict

class diskmap(cmparser):
    def __init__(self):
        self.structure_dict = ordereddict([
            ('name',''),
            ('uniq', ''),
            ])
        self.disk_map = []

    def findPathByName(self, name, commands=['find','/dev', '-name', 'disk_name']):
        commands[3] = name
        pathByName = ''
        out, error = self.execute(commands)
        if error != None:
            raise Exception('There is no zpool avialable, {Error %s}' % error)
            exit(1)
        if out == 'None':
            #could not find path by name
            return -1
        else:
            for line in [i for i in out.splitlines() if i!='']:
                pathByName = line
        return pathByName

    def findIdBySymLinks(self, name, commands = ['find', '-L', '/dev/disk/',\
            '-samefile', 'pathByName']):
        commands[4] = name
        out, error = self.execute(commands)
        if error != None:
            raise Exception('There is no zpool avialable, {Error %s}' % error)
        else:
            ids = {}
            while(len(ids) < 2):
                for line in [i for i in out.splitlines() if i!='']:
                    if line.strip().find('by-path') != -1:
                        ids['by-path'] = line
                    if line.strip().find('by-id') != -1:
                        ids['by-id'] = line
            return ids
    def getdiskMap(self, disks):
        paths, names = [], []
        for name in disks:
            path = self.findPathByName(name)
            if path != '':
               names.append(name)
               paths.append(path)
        print names
        print paths
        for name, path in zip(names,paths):
            ids = self.findIdBySymLinks(path)
            self.structure_dict['name'] = name
            self.structure_dict['uniq'] = ids
            self.disk_map.append(self.structure_dict.copy())
        return self.disk_map

