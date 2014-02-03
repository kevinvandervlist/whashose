'''
Created on 27 Dec 2013

@author: kevin
'''

from messagehandler.basemessagehandler import BaseMessageHandler
from messagehandler.message import Response
import logging

class SuggestionHandler(BaseMessageHandler):
    '''
    Handle suggestions
    '''
    
    def __init__(self, message_handler):
        message_handler.register_handler("suggestion", self)
        self.__log = logging.getLogger(__name__)
            
    def handle_message(self, message, response_queue):
        string = "Thank you for your suggestion. I'll have a look at it."
        
        conn_info = str(message.source_info())
        self.__log.info("Suggestion: " + message.string() + conn_info)
        
        response = Response(string)
        message.set_response(response)
        response_queue.put(message)
    
    def help_message(self):
        return ("suggestion: Make a suggestion to the author of this bot\n")