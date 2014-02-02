'''
Created on 28 Dec 2013

@author: kevin
'''
import unittest
from keywordhandler.tumblrhandler import VrijmiboHandler, TumblrDownloaderStub
from messagehandler.messagehandler import MessageHandlerStub
from messagehandler.message import Message
import queue


class VrijmiboHandlerTest(unittest.TestCase):

    def setUp(self):
        self.stub = MessageHandlerStub()
        tumblr = TumblrDownloaderStub("lingeriebomb")
        self.vrijmibo = VrijmiboHandler(self.stub, tumblr)
        self.queue = queue.Queue()
        
    def make_message(self, string):
        return Message("@", "vrijmibo", string)

    def test_vrijmibo_no_amount(self):
        message = self.make_message("")
        expected = "http://31.media.tumblr.com/f52a7acd069a89ce94fafcca0fb56449/tumblr_mwhpkkZxgg1rg2ka9o1_500.jpg"
        self.vrijmibo.handle_message(message, self.queue)
        response = self.queue.get(False)
        self.assertEqual(expected, response.response().image, "Expcted a different URL")
        self.assertTrue(self.queue.empty(), "Queue should be empty now")

    def test_vrijmibo_1(self):
        message = self.make_message("1")
        expected = "http://31.media.tumblr.com/f52a7acd069a89ce94fafcca0fb56449/tumblr_mwhpkkZxgg1rg2ka9o1_500.jpg"
        self.vrijmibo.handle_message(message, self.queue)
        response = self.queue.get(False)
        self.assertEqual(expected, response.response().image, "Expcted a different URL")
        self.assertTrue(self.queue.empty(), "Queue should be empty now")
        
    def test_vrijmibo_2(self):
        message = self.make_message("3")
        expected = "http://31.media.tumblr.com/f52a7acd069a89ce94fafcca0fb56449/tumblr_mwhpkkZxgg1rg2ka9o1_500.jpg"
        self.vrijmibo.handle_message(message, self.queue)
        
        self.assertEqual(3, self.queue.qsize(), "We should have 3 responses in the queue")
        
        for _ in range(3):
            response = self.queue.get(False)
            self.assertEqual(expected, response.response().image, "Expcted a different URL")
        
        self.assertTrue(self.queue.empty(), "Queue should be empty now")
        
    def test_vrijmibo_more_then_max(self):
        message = self.make_message("2000")
        expected = "http://31.media.tumblr.com/f52a7acd069a89ce94fafcca0fb56449/tumblr_mwhpkkZxgg1rg2ka9o1_500.jpg"
        self.vrijmibo.handle_message(message, self.queue)
        response = self.queue.get(False)
        self.assertEqual(expected, response.response().image, "Expcted a different URL")
        self.assertTrue(self.queue.empty(), "Queue should be empty now")