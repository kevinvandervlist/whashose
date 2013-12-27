'''
Created on 27 Dec 2013

@author: kevin
'''

from abc import ABCMeta, abstractmethod

class BaseMessageHandler(object):
    '''
    Base message handler. Extend this if you want to implement 
    a new message handler for a specific keyword
    '''
    __metaclas__ = ABCMeta

    @abstractmethod
    def handle_message(self, message, response_queue):
        '''
        This method is called when a message containing implementers
        classes' keyword is found.
        '''
        pass
    
    @abstractmethod
    def help_message(self):
        '''
        This method should provide the caller with a help message explaining 
        the supported commands for this message handler
        '''
        pass