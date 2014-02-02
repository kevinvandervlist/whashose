'''
Created on 28 Dec 2013

@author: kevin
'''
import unittest
from keywordhandler.tumblrhandler import VrijmiboHandler, TettenHandler, BoobsClubHandler, TumblrDownloaderStub, TheBoobsClubDownloaderStub
from messagehandler.messagehandler import MessageHandlerStub
from messagehandler.message import Message
import queue


class VrijmiboHandlerTest(unittest.TestCase):

    def setUp(self):
        self.stub = MessageHandlerStub()
        tumblr = TumblrDownloaderStub("lingeriebomb")
        self.expected = "http://31.media.tumblr.com/f52a7acd069a89ce94fafcca0fb56449/tumblr_mwhpkkZxgg1rg2ka9o1_500.jpg"
        self.vrijmibo = VrijmiboHandler(self.stub, tumblr)
        self.queue = queue.Queue()
        
    def make_message(self, string):
        return Message("@", "vrijmibo", string)

    def test_vrijmibo_no_amount(self):
        message = self.make_message("")
        self.vrijmibo.handle_message(message, self.queue)
        response = self.queue.get(False)
        self.assertEqual(self.expected, response.response().image, "Expcted a different URL")
        self.assertTrue(self.queue.empty(), "Queue should be empty now")

    def test_vrijmibo_1(self):
        message = self.make_message("1")
        self.vrijmibo.handle_message(message, self.queue)
        response = self.queue.get(False)
        self.assertEqual(self.expected, response.response().image, "Expcted a different URL")
        self.assertTrue(self.queue.empty(), "Queue should be empty now")
        
    def test_vrijmibo_2(self):
        message = self.make_message("3")
        self.vrijmibo.handle_message(message, self.queue)
        
        self.assertEqual(3, self.queue.qsize(), "We should have 3 responses in the queue")
        
        for _ in range(3):
            response = self.queue.get(False)
            self.assertEqual(self.expected, response.response().image, "Expcted a different URL")
        
        self.assertTrue(self.queue.empty(), "Queue should be empty now")
        
    def test_vrijmibo_more_then_max(self):
        message = self.make_message("2000")
        self.vrijmibo.handle_message(message, self.queue)
        response = self.queue.get(False)
        self.assertEqual(self.expected, response.response().image, "Expcted a different URL")
        self.assertTrue(self.queue.empty(), "Queue should be empty now")
        
class TettenHandlerTest(unittest.TestCase):

    def setUp(self):
        self.stub = MessageHandlerStub()
        tumblr = TumblrDownloaderStub("tettenvrouw")
        self.expected = "http://25.media.tumblr.com/tumblr_m9g9yrtkb21qzt6cxo1_500.jpg"
        self.tetten = TettenHandler(self.stub, tumblr)
        self.queue = queue.Queue()
        
    def make_message(self, string):
        return Message("@", "tetten", string)

    def test_tetten_no_amount(self):
        message = self.make_message("")
        self.tetten.handle_message(message, self.queue)
        response = self.queue.get(False)
        self.assertEqual(self.expected, response.response().image, "Expcted a different URL")
        self.assertTrue(self.queue.empty(), "Queue should be empty now")

    def test_tetten_1(self):
        message = self.make_message("1")
        self.tetten.handle_message(message, self.queue)
        response = self.queue.get(False)
        self.assertEqual(self.expected, response.response().image, "Expcted a different URL")
        self.assertTrue(self.queue.empty(), "Queue should be empty now")
        
    def test_tetten_2(self):
        message = self.make_message("3")
        self.tetten.handle_message(message, self.queue)
        
        self.assertEqual(3, self.queue.qsize(), "We should have 3 responses in the queue")
        
        for _ in range(3):
            response = self.queue.get(False)
            self.assertEqual(self.expected, response.response().image, "Expcted a different URL")
        
        self.assertTrue(self.queue.empty(), "Queue should be empty now")
        
    def test_tetten_more_then_max(self):
        message = self.make_message("2000")
        self.tetten.handle_message(message, self.queue)
        response = self.queue.get(False)
        self.assertEqual(self.expected, response.response().image, "Expcted a different URL")
        self.assertTrue(self.queue.empty(), "Queue should be empty now")
        
class BoobsClubHandlerTest(unittest.TestCase):

    def setUp(self):
        self.stub = MessageHandlerStub()
        tumblr = TheBoobsClubDownloaderStub("theboobsclub")
        self.expected = "http://25.media.tumblr.com/fac67f6d6865034997953bd4e87dbb4b/tumblr_mzrbbpEBSi1to5syao1_500.jpg"
        self.boobsclub = BoobsClubHandler(self.stub, tumblr)
        self.queue = queue.Queue()
        
    def make_message(self, string):
        return Message("@", "boobsclub", string)

    def test_boobsclub_no_amount(self):
        message = self.make_message("")
        self.boobsclub.handle_message(message, self.queue)
        response = self.queue.get(False)
        self.assertEqual(self.expected, response.response().image, "Expcted a different URL")
        self.assertTrue(self.queue.empty(), "Queue should be empty now")

    def test_boobsclub_1(self):
        message = self.make_message("1")
        self.boobsclub.handle_message(message, self.queue)
        response = self.queue.get(False)
        self.assertEqual(self.expected, response.response().image, "Expcted a different URL")
        self.assertTrue(self.queue.empty(), "Queue should be empty now")
        
    def test_boobsclub_2(self):
        message = self.make_message("3")
        self.boobsclub.handle_message(message, self.queue)
        
        self.assertEqual(3, self.queue.qsize(), "We should have 3 responses in the queue")
        
        for _ in range(3):
            response = self.queue.get(False)
            self.assertEqual(self.expected, response.response().image, "Expcted a different URL")
        
        self.assertTrue(self.queue.empty(), "Queue should be empty now")
        
    def test_boobsclub_more_then_max(self):
        message = self.make_message("2000")
        self.boobsclub.handle_message(message, self.queue)
        response = self.queue.get(False)
        self.assertEqual(self.expected, response.response().image, "Expcted a different URL")
        self.assertTrue(self.queue.empty(), "Queue should be empty now")