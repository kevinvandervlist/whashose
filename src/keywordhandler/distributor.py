'''
Created on 2 Feb 2014

@author: kevin
'''

from messagehandler.basemessagehandler import BaseMessageHandler
import logging
import copy
import random

class BaseDistributor(BaseMessageHandler):
    '''
    base handler which will distribute a numbered command over a list of options.
    Use this as a kind of aggregate for various handlers. Do not directly instantiate this class, but subclass it.
    '''
    def __init__(self, message_handler, name, handlers = []):
        self.__message_handler = message_handler
        self.__name = name
        message_handler.register_handler(name, self)
        self.__log = logging.getLogger(__name__)
        self.__handlers = handlers
        self.__magic_token = "@"
        
    def handle_message(self, message, response_queue):
        self.__log.info("handle_message: " + message.string())

        number_of_images = self.validate_number_of_images(10, message.string())
                    
        for x in range(0, number_of_images):
            self.__log.info("distributing command number " + str(x) + " of " + str(number_of_images))
            work = copy.deepcopy(message)
            
            picked_handler = random.choice(self.__handlers)
            
            self.patch_source_info(work, picked_handler)
            
            self.__message_handler.handle(work.source_info(), self.__magic_token + " " + picked_handler + " 1")
            
    def patch_source_info(self, message, new_text):
        """
        Rewrite a message's source info so 
        """
        si = message.source_info()
        si.message = new_text
        message.set_source_info(message)
        
    def help_message(self):
        '''
        This method should provide the caller with a help message explaining 
        the supported commands for this message handler
        '''
        return (self.__name + ": Pick random keywords out of the following list of options\n"
                "  " + str(self.__handlers) + ""
                "  Syntax: @ " + self.__name + " [num]"
                "  Every request has a limit of 10 random handlers."
                "  Example: '@ " + self.__name + " 3'\n")
        

class ChickDistributor(BaseDistributor):
    def __init__(self, message_handler):
        name = "chick"
        handlers = ["vrijmibo", "tetten", "boobsclub", "longview"]
        super(ChickDistributor, self).__init__(message_handler, name, handlers)
        