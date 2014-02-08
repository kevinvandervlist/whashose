'''
Created on 27 Dec 2013

@author: kevin
'''

from connector.whatsapp import WhatsAppImageUploader

class InvalidMessageFormat(Exception):
    '''
    Custom exception, thrown a message is not in a correct format
    '''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class Response(object):
    '''
    Represents a repsonse to a message
    '''
    def __init__(self, string=None, image=None):
        self.string = string
        self.image = image
        
    def handle_string(self, wac, jid, lock):
        def receipt_message_sent(a, b):
            wac.signalInterface.unregisterListener("receipt_messageSent", receipt_message_sent)
            lock.unlock()
        wac.signalInterface.registerListener("receipt_messageSent", receipt_message_sent)
        wac.methodInterface.call("message_send", (jid, self.string))
        
    def handle_image(self, wac, author, jid, lock):
        im_up = WhatsAppImageUploader(author, jid, self.image, wac)
        im_up.upload(lock)

class Message(object):
    '''
    Represents the state of a message within the message handling process
    '''


    def __init__(self, magic_token, keyword, string=""):
        self.__magic_token = magic_token
        self.__keyword = keyword
        self.__string = string
        self.__response = None
        self.__source_info = None
        
    def handle(self, whatsappconnector, lock):
        si = self.source_info()
        response = self.response()
        if response.string is not None:
            response.handle_string(whatsappconnector, si.destination, lock)
        elif response.image is not None:
            response.handle_image(whatsappconnector, si.author, si.destination, lock)
        else:
            msg = "ERROR: Message is not provided with a valid response..."
            raise Exception(msg)
        
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
    
    def response(self):
        '''
        The response that relates to this message
        '''
        return self.__response
    
    def source_info(self):
        '''
        Information on the source of the message. 
        '''
        return self.__source_info
    
    def set_response(self, response):
        self.__response = response
        
    def set_source_info(self, source_info):
        self.__source_info = source_info