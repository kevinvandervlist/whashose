'''
Created on 27 Dec 2013

@author: kevin
'''

import logging
from messagehandler.basemessagehandler import BaseMessageHandler
from messagehandler.message import Message
from messagehandler.message import Response
from messagehandler.message import InvalidMessageFormat

class NoResponseQueueDefined(Exception):
    '''
    Custom exception, thrown when the MessageHandler is not provided with 
    a response queue
    '''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class NoMessageDefined(Exception):
    '''
    Custom exception, thrown when the MessageHandler is not provided with 
    a message to be handled
    '''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class MessageHandlerStub(BaseMessageHandler):
    def register_handler(self, keyword, handler):
        pass
    
class MessageHandler(BaseMessageHandler):
    '''
    Handler to take care of incoming messages.
    There are a few special rules to take into account:
    1) The first token of a sentence must be the 'magic token' provided when
       initialising this class. Messages that do not start with this token
       will be ignored by the message handler
    2) The next word (tokenised by spaces) defines which handler will be 
       invoked in order to take care of this message.
       A special exception is made for the keyword "help", which will ask
       all handlers to supply a help message. This message will be sent 
       to the users that sent the "help" message
    3) The result of a message will be put on the response_queue, which
       is supposed to be manually emptied (for example in a main event
       loop). Otherwise, messages will just built up.
    '''


    def __init__(self, response_queue=None, magic_token = "@"):
        '''
        Constructor
        '''
        self.__log = logging.getLogger(__name__)
        self.__magic_token = magic_token
        self.__handlers = dict(help=self)
        
        if response_queue is None:
            err = "No response queue defined"
            self.__log.error(err)
            raise NoResponseQueueDefined(err)
        self.__response_queue = response_queue
        
    def register_handler(self, keyword, handler):
        '''
        Register a new message handler with a certain keyword
        '''
        if keyword != None and handler != None:
            self.__handlers[keyword] = handler
        
    def handle(self, source_info, message=None):
        '''
        Handle an incoming (e.g. raw) message
        '''
        if message is None:
            err = "Provide a message to handle"
            self.__log.error(err)
            raise NoMessageDefined(err)
        
        if not message.startswith(self.__magic_token):
            return
        
        try:
            tm = self.tokenize(message)
        except InvalidMessageFormat:
            return
        
        tm.set_source_info(source_info)
        
        if tm.magic_token() != self.__magic_token:
            err = "Invalid magic token: " + self.__magic_token + "defined, " \
             + tm.magic_token() + " found in message"
            self.__log.info(err)
            self.__log.info("Discarding message" + message)
            
        self.__handler(tm, source_info)
            
    def __handler(self, tokenized_message, source_info):
        "Actual plumbing with calling handlers or returning notifications about failures"         
        handler = self.__handlers.get(tokenized_message.keyword())
        
        if handler != None:
            try:
                handler.handle_message(tokenized_message, self.__response_queue)
            except:
                self.__log.error("A handler failed with an error, rescue what we can..")
                err = "@ echo Sorry, something went wrong. I can't handle that request right now."
                self.handle(source_info, err)
        else:
            message = "Sorry, I don't understand the command '" + tokenized_message.keyword() + "'. Type '@ help' for a usage information."
            self.__log.info(message)
            err = "@ echo " + message
            self.handle(source_info, err)
        
    def tokenize(self, message):
        s = message.split(' ', 2)
        
        if len(s) is 1:
            err = "Invalid message format -- cannot tokenize: " + message
            self.__log.error(err)
            raise InvalidMessageFormat(err)
        if len(s) is 2:
            return Message(s[0], s[1])
        elif len(s) is 3:
            return Message(s[0], s[1], s[2])
        
    def help_message(self):
        response = ["Usage information:"]
        
        for key in self.__handlers:
            if self.__handlers[key] != self:
                response.append(self.__handlers[key].help_message())
        
        return "\n".join(response)
    
    def handle_message(self, message, response_queue):
        response = Response(self.help_message())
        message.set_response(response)
        
        # Hack: When we send help messages, make sure only the author 
        # gets the message, and not a whole group
        if message.source_info() != None:
            message.source_info().destination = message.source_info().author
        
        response_queue.put(message)