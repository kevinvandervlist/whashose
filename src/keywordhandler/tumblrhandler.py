'''
Created on 28 Dec 2013

@author: kevin
'''

from messagehandler.basemessagehandler import BaseMessageHandler
from messagehandler.message import Response
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import copy
import logging
from urllib.request import urlretrieve
import tempfile

class TumblrDownloader(object):
    def __init__(self, name):
        self.__log = logging.getLogger(__name__)
        self.tumblr = "http://" + name + ".tumblr.com/random/"
        self.suffix = ".jpg"
        
    def file_handle(self, tag):
        soup = bs(urlopen(self.tumblr))
        imgtag = soup.find("img", { "class": tag})
            
        fh = tempfile.NamedTemporaryFile(suffix=self.suffix, delete=False)
        
        urlretrieve(imgtag["src"], fh.name)
        
        return fh
        
    def validate_number_of_images(self, maximum, given):
        number_of_images = 0
        try:
            number_of_images = int(given)
            self.__log.info("Received a request for " + str(number_of_images) + " images.")
            if number_of_images > maximum or number_of_images < 1:
                number_of_images = 1
        except ValueError:
            self.__log.error("Invalid number of images: setting 1")
            number_of_images = 1
        return number_of_images        

class TettenHandler(BaseMessageHandler):
    '''
    Handler for tettenvrouw
    '''
    def __init__(self, message_handler):
        message_handler.register_handler("tetten", self)
        self.__log = logging.getLogger(__name__)
        
    def handle_message(self, message, response_queue):
        self.__log.info("handle_message: " + message.string())
        tumblr = TumblrDownloader("tettenvrouw")

        number_of_images = tumblr.validate_number_of_images(15, message.string())
                    
        for x in range(0, number_of_images):
            self.__log.info("Getting image number " + str(x) + " of " + str(number_of_images))
            work = copy.deepcopy(message)
            
            fh = tumblr.file_handle("main_photo")
        
            response = Response(image=fh)
            work.set_response(response)
            response_queue.put(work)
        
    def help_message(self):
        '''
        This method should provide the caller with a help message explaining 
        the supported commands for this message handler
        '''
        return ("tetten: Tettenvrouw (ook vrijmibo)\n"
                "  Syntax: @ tetten [num]"
                "  Stuur willekeurige tettenvrouw-fotos op!\n"
                "  Op iedere 'aanvraag' zit een limiet van 15 fotos."
                "  Voorbeeld: '@ tetten 3' voor 3 fotos\n")

class VrijmiboHandler(BaseMessageHandler):
    '''
    The vrijmibo handler
    '''
    
    def __init__(self, message_handler):
        message_handler.register_handler("vrijmibo", self)
        self.__log = logging.getLogger(__name__)
            
    def handle_message(self, message, response_queue):
        '''
        Go and fetch a certain amound of random vrijmibo-worthy photos
        '''
        self.__log.info("handle_message: " + message.string())
        tumblr = TumblrDownloader("lingeriebomb")

        number_of_images = tumblr.validate_number_of_images(15, message.string())
            
        for x in range(0, number_of_images):
            self.__log.info("Getting image number " + str(x) + " of " + str(number_of_images))
            work = copy.deepcopy(message)
            
            fh = tumblr.file_handle("notPhotoset")
        
            response = Response(image=fh)
            work.set_response(response)
            response_queue.put(work)
    
    def help_message(self):
        '''
        This method should provide the caller with a help message explaining 
        the supported commands for this message handler
        '''
        return ("vrijmibo: De vrijdag middag borrel\n"
                "  Syntax: @ vrijmibo [num]"
                "  Stuur willekeurige vrijmibo-fotos op!\n"
                "  Op iedere 'aanvraag' zit een limiet van 15 fotos."
                "  Voorbeeld: '@ vrijmibo 3' voor 3 fotos\n")