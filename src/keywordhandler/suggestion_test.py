'''
Created on 28 Dec 2013

@author: kevin
'''
import unittest
from keywordhandler.echohandler import EchoHandler
from messagehandler.messagehandler import MessageHandlerStub
from messagehandler.message import Message
import queue


class EchoHandlerTest(unittest.TestCase):

    def setUp(self):
        self.stub = MessageHandlerStub()
        self.echo = EchoHandler(self.stub)
        self.queue = queue.Queue()
        
    def make_message(self, string):
        return Message("@", "suggestionhandler", string)
    

    def test_suggestion(self):
        message = self.make_message("mijn suggestie")
        self.echo.handle_message(message, self.queue)
        response = self.queue.get()
        self.assertEqual(message.string(), response.response().string, "Strings should be equal")