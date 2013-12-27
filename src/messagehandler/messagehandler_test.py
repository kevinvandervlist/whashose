'''
Created on 27 Dec 2013

@author: kevin
'''
import unittest
import queue
from messagehandler.messagehandler import NoResponseQueueDefined
from messagehandler.messagehandler import NoMessageDefined
from messagehandler.messagehandler import MessageHandler
from messagehandler.message import InvalidMessageFormat


class Test(unittest.TestCase):


    def setUp(self):
        q = queue.Queue
        self.mh = MessageHandler(q)
        self.message_a = "@ help blabla"
        self.message_b = "@ foo"
        self.message_c = "@"

    def tearDown(self):
        pass

    def test_no_response_queue_defined(self):
        self.assertRaises(NoResponseQueueDefined, lambda: MessageHandler())

    def test_response_queue_defined(self):
        q = queue.Queue()
        MessageHandler(q)
        self.assertTrue(True, "No exception should be raised")
        
    def test_no_message_defined(self):
        self.assertRaises(NoMessageDefined, lambda: self.mh.handle())
        
        
        
    def test_tokenize_message_a(self):
        t = self.mh.tokenize(self.message_a)
        self.assertEqual("@", t.magic_token(), "Magic token must be '@'")
        self.assertEqual("help", t.keyword(), "Keyword must be 'help'")
        self.assertEqual("blabla", t.string(), "String must be 'blabla'")
        
    def test_message_a_defined(self):
        self.mh.handle(self.message_a)
        self.assertTrue(False)
        
        
        
    def test_tokenize_message_b(self):
        t = self.mh.tokenize(self.message_b)
        self.assertEqual("@", t.magic_token(), "Magic token must be '@'")
        self.assertEqual("foo", t.keyword(), "Keyword must be 'foo'")
        self.assertEqual("", t.string(), "String must be empty")

    def test_message_b_defined(self):
        self.mh.handle(self.message_b)
        self.assertTrue(False)
        
        
        
    def test_tokenize_message_c(self):
        self.assertRaises(InvalidMessageFormat, lambda: self.mh.tokenize(self.message_c))
        
    def test_message_c_defined(self):
        self.assertRaises(InvalidMessageFormat, lambda: self.mh.handle(self.message_c))
        

        
    def test_nondefault_magic_token(self):
        message = "# foo bar baz"
        mh = MessageHandler(response_queue = queue.Queue, magic_token = "#")
        mh.handle(message)
        self.assertTrue(False)