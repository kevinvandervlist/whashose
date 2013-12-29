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
        return Message("@", "echo", string)
    
    def test_echo_no_word(self):
        message = self.make_message("")
        self.echo.handle_message(message, self.queue)
        response = self.queue.get()
        self.assertEqual(message.string(), response.response().string, "Strings should be equal")

    def test_echo_single_word(self):
        message = self.make_message("foo")
        self.echo.handle_message(message, self.queue)
        response = self.queue.get()
        self.assertEqual(message.string(), response.response().string, "Strings should be equal")
        
    def test_echo_simple_string(self):
        message = self.make_message("a string")
        self.echo.handle_message(message, self.queue)
        response = self.queue.get()
        self.assertEqual(message.string(), response.response().string, "Strings should be equal")
        
    def test_echo_complex_string(self):
        message = self.make_message("a 'tnhNTHO7 7 +o+o!] -sl{- {-[-{ eosntaau")
        self.echo.handle_message(message, self.queue)
        response = self.queue.get()
        self.assertEqual(message.string(), response.response().string, "Strings should be equal")    