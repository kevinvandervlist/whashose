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

class VrijmiboHandler(BaseMessageHandler):
    '''
    An echo handler
    '''
    
    def __init__(self, message_handler):
        message_handler.register_handler("vrijmibo", self)
        self.__log = logging.getLogger(__name__)
            
    def handle_message(self, message, response_queue):
        '''
        Go and fetch a certain amound of random vrijmibo-worthy photos
        '''
        self.__log.info("handle_message: " + message.string())
        number_of_images = 0
        try:
            number_of_images = int(message.string())
            self.__log.info("Received a request for " + str(number_of_images) + " images.")
            if number_of_images > 15 or number_of_images < 1:
                number_of_images = 1
        except ValueError:
            self.__log.info("Invalid number of images: setting 1")
            number_of_images = 1
            
        for x in range(0, number_of_images):
            self.__log.info("Getting image number " + str(x) + " of " + str(number_of_images))
            work = copy.deepcopy(message)
            url="http://lingeriebomb.tumblr.com/random/"
            soup = bs(urlopen(url))
            img = soup.find("img", { "class": "notPhotoset"})
            #img, _ = urlretrieve(img["src"])
        
            response = Response(image=img["src"])
            work.set_response(response)
            response_queue.put(work)
    
    def help_message(self):
        '''
        This method should provide the caller with a help message explaining 
        the supported commands for this message handler
        '''
        return ("vrijmibo: De vrijdag middag borrel\n"
                "  Stuur willekeurige vrijmibo-fotos op!\n"
                "  Op iedere 'aanvraag' zit een limiet van 15 fotos."
                "  Voorbeeld: '@ vrijmibo 3' voor 3 fotos\n")