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
import os

class BaseTumblrDownloader(object):
    def __init__(self):
        self.__log = logging.getLogger(__name__)
        
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

class TumblrDownloader(BaseTumblrDownloader):
    def __init__(self, name):
        self.__log = logging.getLogger(__name__)
        self.tumblr = "http://" + name + ".tumblr.com/random/"
        self.suffix = ".jpg"
        super(TumblrDownloader, self).__init__()

    def get_imgtag(self, tag):
        soup = bs(urlopen(self.tumblr))
        return soup.find("img", { "class": tag})
        
    def file_handle(self, tag):
        imgtag = self.get_imgtag(tag)

        if imgtag is None:
            return None

        fh = tempfile.NamedTemporaryFile(suffix=self.suffix, delete=False)
        
        urlretrieve(imgtag["src"], fh.name)
        
        return fh

class TumblrDownloaderStub(BaseTumblrDownloader):
    """ 
    Stub implementation of the tumblr downloader for testing
    """
    def __init__(self, name):
        # the test file path:
        self.tumblr_file = os.path.dirname(__file__) + "/../../testdata/" + name + ".tumblr.com"
        super(TumblrDownloaderStub, self).__init__()
    
    def get_imgtag(self, tag):
        fh = open(self.tumblr_file)
        soup = bs(fh)
        s = soup.find("img", {"class": tag})
        fh.close()
        return s
    
    def file_handle(self, tag):
        imgtag = self.get_imgtag(tag)
        if imgtag is None:
            return None
        return imgtag["src"]
    
    
class TheBoobsClubDownloader(TumblrDownloader):
    def __init__(self, name):
        super(TheBoobsClubDownloader, self).__init__(name)

    def get_imgtag(self, tag):
        soup = bs(urlopen(self.tumblr))
        div = soup.find("div", { "class": tag})
        return div.find("img")

class TheBoobsClubDownloaderStub(TumblrDownloaderStub):
    def __init__(self, name):
        super(TheBoobsClubDownloaderStub, self).__init__(name)

    def get_imgtag(self, tag):
        fh = open(self.tumblr_file)
        soup = bs(fh)
        div = soup.find("div", {"class": tag})
        img = div.find("img")
        fh.close()
        return img
    
class TheLongerViewDownloader(TumblrDownloader):
    def __init__(self, name):
        super(TheLongerViewDownloader, self).__init__(name)

    def get_imgtag(self, tag):
        soup = bs(urlopen(self.tumblr))
        img = soup.find("img", { "class": tag})
        img["src"] = img["data-original"]
        return img

class TheLongerViewDownloaderStub(TumblrDownloaderStub):
    def __init__(self, name):
        super(TheLongerViewDownloaderStub, self).__init__(name)

    def get_imgtag(self, tag):
        fh = open(self.tumblr_file)
        soup = bs(fh)
        img = soup.find("img", {"class": tag})
        img["src"] = img["data-original"]
        fh.close()
        return img
    
class TettenHandler(BaseMessageHandler):
    '''
    Handler for tettenvrouw
    '''
    def __init__(self, message_handler, tumblr = TumblrDownloader("tettenvrouw")):
        message_handler.register_handler("tetten", self)
        self.__log = logging.getLogger(__name__)
        self.tumblr = tumblr
        
    def handle_message(self, message, response_queue):
        self.__log.info("handle_message: " + message.string())

        number_of_images = self.tumblr.validate_number_of_images(10, message.string())
                    
        for x in range(0, number_of_images):
            self.__log.info("Getting image number " + str(x) + " of " + str(number_of_images))
            work = copy.deepcopy(message)
            
            fh = None
            tries = 0
            while fh is None and tries < 3:
                fh = self.tumblr.file_handle("main_photo")
                tries+=1
        
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
                "  Op iedere 'aanvraag' zit een limiet van 10 fotos."
                "  Voorbeeld: '@ tetten 3' voor 3 fotos\n")

class VrijmiboHandler(BaseMessageHandler):
    '''
    The vrijmibo handler
    '''
    
    def __init__(self, message_handler, tumblr = TumblrDownloader("lingeriebomb")):
        message_handler.register_handler("vrijmibo", self)
        self.__log = logging.getLogger(__name__)
        self.tumblr = tumblr
            
    def handle_message(self, message, response_queue):
        '''
        Go and fetch a certain amount of random vrijmibo-worthy photos
        '''
        self.__log.info("handle_message: " + message.string())

        number_of_images = self.tumblr.validate_number_of_images(10, message.string())
            
        for x in range(0, number_of_images):
            self.__log.info("Getting image number " + str(x) + " of " + str(number_of_images))
            work = copy.deepcopy(message)
            
            fh = None
            tries = 0
            while fh is None and tries < 3:
                fh = self.tumblr.file_handle("notPhotoset")
                tries+=1
        
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
                "  Op iedere 'aanvraag' zit een limiet van 10 fotos."
                "  Voorbeeld: '@ vrijmibo 3' voor 3 fotos\n")

class BoobsClubHandler(BaseMessageHandler):
    '''
    The boobsclub handler voor VVGA
    '''
    
    def __init__(self, message_handler, tumblr = TheBoobsClubDownloader("theboobsclub")):
        message_handler.register_handler("boobsclub", self)
        self.__log = logging.getLogger(__name__)
        self.tumblr = tumblr
            
    def handle_message(self, message, response_queue):
        self.__log.info("handle_message: " + message.string())

        number_of_images = self.tumblr.validate_number_of_images(10, message.string())
            
        for x in range(0, number_of_images):
            self.__log.info("Getting image number " + str(x) + " of " + str(number_of_images))
            work = copy.deepcopy(message)
            
            fh = None
            tries = 0
            while fh is None and tries < 3:
                fh = self.tumblr.file_handle("the-photo")
                tries+=1
        
            response = Response(image=fh)
            work.set_response(response)
            response_queue.put(work)
    
    def help_message(self):
        '''
        This method should provide the caller with a help message explaining 
        the supported commands for this message handler
        '''
        return ("boobsclub: theboobsclub voor VVGA\n"
                "  Syntax: @ boobsclub [num]"
                "  Op iedere 'aanvraag' zit een limiet van 10 fotos."
                "  Voorbeeld: '@ longview 3' voor 3 fotos\n")

class TheLongerViewHandler(BaseMessageHandler):
    def __init__(self, message_handler, tumblr = TheLongerViewDownloader("thelongerview")):
        message_handler.register_handler("longview", self)
        self.__log = logging.getLogger(__name__)
        self.tumblr = tumblr
            
    def handle_message(self, message, response_queue):
        self.__log.info("handle_message: " + message.string())

        number_of_images = self.tumblr.validate_number_of_images(10, message.string())
            
        for x in range(0, number_of_images):
            self.__log.info("Getting image number " + str(x) + " of " + str(number_of_images))
            work = copy.deepcopy(message)
            
            fh = None
            tries = 0
            while fh is None and tries < 3:
                fh = self.tumblr.file_handle("focus")
                tries+=1
        
            response = Response(image=fh)
            work.set_response(response)
            response_queue.put(work)
    
    def help_message(self):
        return ("longerview: The long view\n"
                "  Syntax: @ longview [num]"
                "  Stuur willekeurige vrijmibo-fotos op!\n"
                "  Op iedere 'aanvraag' zit een limiet van 10 fotos."
                "  Voorbeeld: '@ vrijmibo 3' voor 3 fotos\n")