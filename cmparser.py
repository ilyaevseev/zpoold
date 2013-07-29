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
        self.structure_dict = ordereddict({ 
                    'name':'',
                    'full_size':'',
                    'm_size':'',
                    'full_size2':'',
                    'usage':'',
                    'speed':'',
                    'status':'',
                    'other_part':'',
                    })
    def get_zpool_list_h(self, commands = ['zpool', 'list', '-H']):
        out, error = self.execute(commands)
        if error !='' or None:
            raise Exception('There is no zpool avialable')
            exit(2)
        else:
            for line in out.splitlines():
                for word in line.split(None):
                    for key in self.structure_dict.keys():
                        self.structure_dict[key] = word
                self.list_of_structures.append(self.structure_dict)        
                #TODO parse out structure
            return self.list_of_structures

class zpool_autoreplace(cmparser):
    def __init__(self):
        self.structure_dict = ordereddict({ 
                    'name':'',
                    'property':'',
                    'value':'',
                    'source':'',
                    })
    def get_autoreplace(self, commands = ['zpool','get','autoreplace']):
        out, error = self.execute(commands)
        if error !='' or None:
            raise Exception('There is no zpool avialable')
            exit(2)
        else:
            pass
        #TODO fill the structure 

class zpool_status(cmparser):
    def __init__(self):
        self.structure_dict = ordereddict({ 
            'pool':'',
            'state':'',
            'scan':'',
            'config': {'name':'',
                'state':'',
                'read':'',
                'write':'',
                'cssum':'',
                }
            })
    def get_zpool_status(self, zpool_name, commands = ['zpool','status', 'zpool_name', '-v']):
        commands[2] = zpool_name
        out, error = self.execute(commands)
        if error !='' or None:
            raise Exception('There is no zpool avialable')
            exit(2)
        else:
            pass
    
