'''
Created on 27 Dec 2013

@author: kevin
'''
import unittest
import queue
from messagehandler.messagehandler import NoResponseQueueDefined
from messagehandler.messagehandler import NoMessageDefined
from messagehandler.messagehandler import MessageHandler
from keywordhandler.echohandler import EchoHandler


class Test(unittest.TestCase):


    def setUp(self):
        self.queue = queue.Queue()
        self.mh = MessageHandler(self.queue)
        
        # Register the echo handler as well
        EchoHandler(self.mh)
        
        self.message_a = "@ help blabla"
        self.message_b = "@ foo"
        self.message_c = "@ echo my_echo"

    def tearDown(self):
        pass

    def test_no_response_queue_defined(self):
        self.assertRaises(NoResponseQueueDefined, lambda: MessageHandler())

    def test_response_queue_defined(self):
        q = queue.Queue()
        MessageHandler(q)
        self.assertTrue(True, "No exception should be raised")
        
    def test_no_message_defined(self):
        self.assertRaises(NoMessageDefined, lambda: self.mh.handle(None, None))
        
        
        
    def test_tokenize_message_a(self):
        t = self.mh.tokenize(self.message_a)
        self.assertEqual("@", t.magic_token(), "Magic token must be '@'")
        self.assertEqual("help", t.keyword(), "Keyword must be 'help'")
        self.assertEqual("blabla", t.string(), "String must be 'blabla'")
        
    def test_message_a_defined(self):
        self.mh.handle(None, self.message_a)
        m = self.queue.get()
        self.assertTrue(m.response().string.startswith("Usage information"), "Should provide usage information")
        
        
        
    def test_tokenize_message_b(self):
        t = self.mh.tokenize(self.message_b)
        self.assertEqual("@", t.magic_token(), "Magic token must be '@'")
        self.assertEqual("foo", t.keyword(), "Keyword must be 'foo'")
        self.assertEqual("", t.string(), "String must be empty")

    def test_message_b_defined(self):
        self.mh.handle(None, self.message_b)
        m = self.queue.get()
        self.assertTrue(m.response().string.startswith("Sorry, I don't understand the command"), "Should provide usage information")
        self.assertTrue(self.queue.empty())
        
        
        
    def test_tokenize_message_c(self):
        t = self.mh.tokenize(self.message_c)
        self.assertEqual("@", t.magic_token(), "Magic token must be '@'")
        self.assertEqual("echo", t.keyword(), "Keyword must be 'echo'")
        self.assertEqual("my_echo", t.string(), "String must be 'my_echo'")
        
    def test_message_c_defined(self):
        self.mh.handle(None, self.message_c)
        m = self.queue.get()
        self.assertEqual(m.response().string, "my_echo", "Should use the echo handler")
        

        
    def test_nondefault_magic_token(self):
        message = "# echo bar baz"
        q = queue.Queue()
        mh = MessageHandler(response_queue = q, magic_token = "#")
        EchoHandler(mh)
        
        mh.handle(None, message)
        m = q.get()
        self.assertEqual(m.response().string, "bar baz", "Should use the echo handler")