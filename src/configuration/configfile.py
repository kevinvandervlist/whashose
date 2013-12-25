'''
Created on 25 Dec 2013

@author: kevin
'''

import os

class ConfigFile(object):
    '''
    classdocs
    '''


    def __init__(self, configfile):
        '''
        Courtesy of Yowsup-CLI
        '''
        if os.path.isfile(configfile):
            f = open(configfile)
        
        self.phonenumber = ""
        self.password = ""
        
        try:
            for l in f:
                line = l.strip()
                if len(line) and line[0] not in ('#', ';'):
                    
                    prep = line.split('#', 1)[0].split(';', 1)[0].split('=', 1)
                    
                    varname = prep[0].strip()
                    val = prep[1].strip()
                    
                    if varname == "phone":
                        self.phonenumber = val
                    elif varname == "password":
                        self.password = val
            return                
        except:
            pass
        
        print("Cannot read a valid configuration file!")


    def isValid(self):
        return self.password != "" and self.phonenumber != ""