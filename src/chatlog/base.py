'''
Created on 3 Feb 2014

@author: kevin
'''

from abc import ABCMeta, abstractmethod
import logging

class BaseStatisticsEntry(object):
    '''
    Base class for chatlog entries. Subclass this in order to create specific chatlog objects
    '''
    __metaclas__ = ABCMeta
    
    def __init__(self):
        self.__log = logging.getLogger(__name__)

    @abstractmethod
    def save(self):
        raise Exception("Not implemented yet")