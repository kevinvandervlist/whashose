'''
Created on 3 Feb 2014

@author: kevin
'''

from chatlog.base import BaseStatisticsEntry
from abc import ABCMeta
import logging

class SetupLog(object):
    def __init__(self):
        l = logging.getLogger("CHATLOG")
        formatter = logging.Formatter('%(asctime)s : %(message)s')
        fileHandler = logging.FileHandler("/var/log/whashose-chats.log", mode='a')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)

        l.setLevel(logging.INFO)
        l.addHandler(fileHandler)
        l.addHandler(streamHandler)

class BaseMessageStatistics(BaseStatisticsEntry):
    
    __metaclas__ = ABCMeta
    
    def __init__(self, message = None, source_jid = None, push_name = None, timestamp = None, author = source_jid):
        super(BaseMessageStatistics, self).__init__()
        self.__message = message
        self.__source_jid = source_jid
        self.__author = author
        self.__timestamp = timestamp
        self.__push_name = push_name
        
    def message(self):
        return self.__message
    
    def set_message(self, message):
        self.__message = message
        
    def source_jid(self):
        return self.__source_jid
    
    def set_source_jid(self, jid):
        self.__source_jid = jid
        
    def author(self):
        return self.__author
    
    def set_author(self, author):
        self.__author = author
    
    def timestamp(self):
        return self.__timestamp
    
    def set_timestamp(self, timestamp):
        return self.__timestamp
    
    def push_name(self):
        return self.__pushname
    
    def set_push_name(self, name):
        self.__push_name = name
                
class GroupMessageStatistics(BaseMessageStatistics):
    def __init__(self, message, source_jid, push_name, timestamp, author):
        super(GroupMessageStatistics, self).__init__(message, source_jid, push_name, timestamp, author)
        
    def store(self):
        log = logging.getLogger("CHATLOG")
        log.info("Group Message," + str(self))
        
    def __str__(self):
        str(self.__message) + "," + str(self.__source_jid) + "," + str(self.__push_name) + "," + str(self.__timestamp) + "," + str(self.__author) 


class MessageStatistics(BaseMessageStatistics):
    def __init__(self, message = None, source_jid = None, push_name = None, timestamp = None):
        super(MessageStatistics, self).__init__(message, source_jid, push_name, timestamp)

    def store(self):
        log = logging.getLogger("CHATLOG")
        log.info("Message," + str(self))
        
    def __str__(self):
        str(self.__message) + "," + str(self.__source_jid) + "," + str(self.__push_name) + "," + str(self.__timestamp) + "," + str(self.__author)