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

class CyanideAndHappinessDownloader(object):
    def __init__(self):
        self.__log = logging.getLogger(__name__)
        self.randomurl = "http://explosm.net/comics/random/"
        self.latesturl = "http://explosm.net/comics/new/"
        self.suffix = ".jpg"
        
    def file_handle(self, latest=None):
        url = self.randomurl
        if latest:
            url = self.latesturl
        soup = bs(urlopen(url))
        title = str(soup.html.head.title.string)
        
        if title == "404 Not Found":
            soup = bs(urlopen(self.xkcdrandom))
                   
        imgtag = soup.find("img", { "alt": "Cyanide and Happiness, a daily webcomic" })
            
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
            self.__log.error("Invalid number of images: getting the latest comic")
            number_of_images = None
        return number_of_images    

class CyanideAndHappinessHandler(BaseMessageHandler):
    '''
    The Cyanide and Happiness handler
    '''
    
    def __init__(self, message_handler):
        message_handler.register_handler("ch", self)
        self.__log = logging.getLogger(__name__)
            
    def handle_message(self, message, response_queue):
        '''
        Go and fetch a certain amount of Cyanide and Happiness comics
        '''
        self.__log.info("handle_message: " + message.string())
        ch = CyanideAndHappinessDownloader()
            
        work = copy.deepcopy(message)
        
        if message.string() is "":
            # Get the latest comic
            fh = ch.file_handle(latest=True)
            response = Response(image=fh)
            work.set_response(response)
            response_queue.put(work)
        else:
            # Otherwise, get a certain ammount
            number_of_images = ch.validate_number_of_images(15, message.string())
            
            for x in range(0, number_of_images):
                self.__log.info("Getting CH image number " + str(x) + " of " + str(number_of_images))
                work = copy.deepcopy(message)
                
                fh = None
                tries = 0
                while fh is None and tries < 3:
                    fh = ch.file_handle()
                    tries+=1
        
                response = Response(image=fh)
                work.set_response(response)
                response_queue.put(work)
    
    def help_message(self):
        '''
        This method should provide the caller with a help message explaining 
        the supported commands for this message handler
        '''
        return ("ch: Get a Cyanide and Happiness comic"
                "  Syntax: @ ch [num]"
                "  Sent a certain amount of random CH comics\n"
                "  Example: '@ ch 3' For three random comics\n")