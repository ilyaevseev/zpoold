'''
base class for stdout parse
'''
import subprocess 
from sys import exit
from collections import OrderedDict as ordereddict

class cmparser(object):
    def __init__(self):
        self.list_of_structures = []
    def execute(self, commands):
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
    def get_zpool_list_h(self, commands = ['zpool', 'list', '-H']):
        out, error = self.execute(commands)
        if error !='' or None:
            raise Exception('There is no zpool avialable, {Error %s}' % error)
            exit(1)
        else:
            for line in out.splitlines()[1:]:
                for key, word in zip(self.structure_dict.keys(),line.split(None)):
                    self.structure_dict[key] = word
                self.list_of_structures.append(self.structure_dict)
            return self.list_of_structures

class zpool_autoreplace(cmparser):
    def __init__(self):
        self.structure_dict = ordereddict([
                    ('name',''),
                    ('property',''),
                    ('status',''),
                    ('value',''),
                    ('source',''),
                    ])
    def get_autoreplace(self, commands = ['zpool','get','autoreplace']):
        out, error = self.execute(commands)
        if error !='' or None:
            raise Exception('There is no zpool avialable, {Error %s}' % error)
            exit(1)
        else:
            for line in out.splitlines()[1:]:
                for key, word in zip(self.structure_dict.keys(),line.split(None)):
                    self.structure_dict[key] = word
                self.list_of_structures.append(self.structure_dict)
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
    def get_zpool_status(self, zpool_name, commands = ['zpool','status', 'zpool_name', '-v']):
        commands[2] = zpool_name
        out, error = self.execute(commands)
        if error !='' or None:
            raise Exception('There is no zpool avialable, {Error %s}' % error)
            exit(1)
        else:
            stopwords = self.structure_dict.keys()
            prev_word = ''; i, g = 0,0
            config = []; error = []
            for line in out.splitlines():
                row = line.split(None)
                if len(row) > 0:
                    cur_word = row[0][:-1]
                    if row[0][:-1] in stopwords:
                        if row[0][:-1] == 'pool':
                            self.structure_dict['pool'] = row[1]
                            prev_word = 'pool'
                        elif row[0][:-1] == 'state':
                            self.structure_dict['state'] = row[1]
                            prev_word = 'state'
                        elif row[0][:-1] == 'state':
                            self.structure_dict['scan'] = row[1]
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
                                config.append(self.config)
                        if prev_word == 'errors':
                            error.append(row)
            self.structure_dict['errors'].append(error)
            self.structure_dict['config'].append(config)
            i,g = 0,0
            return self.structure_dict

