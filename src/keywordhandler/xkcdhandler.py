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

class XkcdDownloader(object):
    def __init__(self):
        self.__log = logging.getLogger(__name__)
        self.xkcdrandom = "http://dynamic.xkcd.com/random/comic/"
        self.xkcdbase = "http://xkcd.com/"
        self.suffix = ".jpg"
        
    def file_handle(self, number=None):
        url = self.xkcdrandom
        if number is not None:
            url = self.xkcdbase + str(number)
        
        soup = bs(urlopen(url))
        title = str(soup.html.head.title.string)
        
        if title == "404 Not Found":
            soup = bs(urlopen(self.xkcdrandom))
            
        comic_title = soup.find("title").text
            
        imgdiv = soup.find("div", { "id": "comic"})
        imgtag = imgdiv.find("img")
            
        fh = tempfile.NamedTemporaryFile(suffix=self.suffix, delete=False)
        
        urlretrieve(imgtag["src"], fh.name)
        
        return (fh, comic_title + "\n" + imgtag["title"])
        
    def validate_number(self, given):
        number_of_images = 0
        try:
            number_of_images = int(given)
            self.__log.info("Received a request for comic " + str(number_of_images))
        except ValueError:
            self.__log.info("Invalid number of images: setting 1")
            number_of_images = None
        return number_of_images        

class XkcdHandler(BaseMessageHandler):
    '''
    The XKCD handler
    '''
    
    def __init__(self, message_handler):
        message_handler.register_handler("xkcd", self)
        self.__log = logging.getLogger(__name__)
            
    def handle_message(self, message, response_queue):
        '''
        Go and fetch a certain amound of random vrijmibo-worthy photos
        '''
        self.__log.info("handle_message: " + message.string())
        xkcd = XkcdDownloader()

        comic_number = xkcd.validate_number(message.string())
            
        work = copy.deepcopy(message)
            
        (fh, text) = xkcd.file_handle(comic_number)
        
        # Return image
        response = Response(image=fh)
        work.set_response(response)
        # And text
        response = Response(string=text)
        message.set_response(response)
        
        response_queue.put(message)
        response_queue.put(work)
    
    def help_message(self):
        '''
        This method should provide the caller with a help message explaining 
        the supported commands for this message handler
        '''
        return ("xkcd: Get a XKCD comic"
                "  Syntax: @ XKCD [num]"
                "  Sent a random or specific (by id) comic\n"
                "  Example: '@ xkcd 149' For make me a sandwich\n")