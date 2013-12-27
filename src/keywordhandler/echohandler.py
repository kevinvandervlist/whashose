'''
Created on 27 Dec 2013

@author: kevin
'''

from messagehandler.basemessagehandler import BaseMessageHandler
from messagehandler.message import Response

class EchoHandler(BaseMessageHandler):
    '''
    An echo handler
    '''
    
    def __init__(self, message_handler):
        message_handler.register_handler("echo", self)
            
    def handle_message(self, message, response_queue):
        '''
        This method is called when a message containing implementers
        classes' keyword is found.
        '''
        
        response = Response(message.string())
        message.set_response(response)
        response_queue.put(message)
    
    def help_message(self):
        '''
        This method should provide the caller with a help message explaining 
        the supported commands for this message handler
        '''
        return ("echo: An Echo Handler\n"
                "  This is a basic command handler that will only\n"
                "  sent you back whatever string you provided\n"
                "  Example usage: '@ echo This will be the response'\n")