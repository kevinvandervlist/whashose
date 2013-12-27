'''
Created on 27 Dec 2013

@author: kevin
'''

class InvalidMessageFormat(Exception):
    '''
    Custom exception, thrown a message is not in a correct format
    '''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Message(object):
    '''
    Represents the state of a message within the message handling process
    '''


    def __init__(self, magic_token, keyword, string=""):
        self.__magic_token = magic_token
        self.__keyword = keyword
        self.__string = string
        
    def magic_token(self):
        '''
        The magic token used to identify this message
        '''
        return self.__magic_token
    
    def keyword(self):
        '''
        The keyword given to this message
        '''
        return self.__keyword
    
    def string(self):
        '''
        The actual text of this message
        '''
        return self.__string