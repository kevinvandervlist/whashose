'''
Created on 28 Dec 2013

@author: kevin
'''
import unittest
from keywordhandler.vrijmibohandler import VrijmiboHandler
from messagehandler.messagehandler import MessageHandlerStub
from messagehandler.message import Message
import queue


class VrijmiboHandlerTest(unittest.TestCase):

    def setUp(self):
        self.stub = MessageHandlerStub()
        self.echo = VrijmiboHandler(self.stub)
        self.queue = queue.Queue()
        
    def make_message(self, string):
        return Message("@", "vrijmibo", string)

    def test_echo_no_amount(self):
        return
        message = self.make_message("")
        self.echo.handle_message(message, self.queue)
        response = self.queue.get(False)
        self.assertEqual(message.string(), response.response().string, "Strings should be equal")
            