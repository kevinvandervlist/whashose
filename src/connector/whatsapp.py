'''
Created on 26 Dec 2013

@author: kevin
'''

import logging
import base64

from Yowsup.connectionmanager import YowsupConnectionManager

class WhatsAppConnector(object):
    '''
    classdocs
    '''


    def __init__(self, phonenumber=None, password=None, autopong=True):
        '''
        Constructor
        '''
        self.__log = logging.getLogger(__name__)
        
        if phonenumber is None:
            self.__log.error("No phonenumber given.")
            return
        if password is None:
            self.__log.error("No password given.")
            return
        
        self.__phonenumber = phonenumber
        self.__password = self.__encode_password(password)
        
        self.__connection_manager = YowsupConnectionManager()
        self.__connection_manager.setAutoPong(autopong)
        
        self.signalInterface = self.__connection_manager.getSignalsInterface()
        self.methodInterface = self.__connection_manager.getMethodsInterface()
        
        self.__register_default_listeners()
        
    def __register_default_listeners(self):
        '''
        Register a few default listeners.
        These are used for the basic things like authentication and disconnecting
        '''
        self.signalInterface.registerListener("auth_fail", self.__on_auth_failed)
        self.signalInterface.registerListener("auth_success", self.__on_auth_success)
        self.signalInterface.registerListener("disconnected", self.__on_disconnected)
        
        
    def __encode_password(self, password):
        '''
        Yowsup requires a specific password representation.
        Use this function to create a correct byte-representation 
        of a UTF-8 string password
        '''
        pwbytes = bytes(password.encode('utf-8'))
        return base64.b64decode(pwbytes)

    def connect(self):
        '''
        Connect to the WhatsApp servers and try to authenticate
        '''
        self.methodInterface.call("auth_login", (self.__phonenumber, self.__password))
        
    def ready(self):
        '''
        Calling this method will signal the WhatsApp servers we are ready to start communicating. 
        Call this after finishing setting up event handlers you are interested in.
        '''
        self.methodInterface.call("ready")
        
    def disconnect(self, reason="User gave no reason"):
        '''
        Disconnect from the WhatsApp servers
        '''
        self.__log.info("User ", self.__phonenumber, " will try to disconnect because of reason: ", reason)
        self.methodInterface.call("disconnect", (reason, ))
    
    def __on_auth_success(self, username):
        self.__log.info("User ", username, " successfully logged in.")
        
    def __on_auth_failed(self, username, err):
        self.__log.error("Can't login ", username, " because of error: ", err)
        
    def __on_disconnected(self, reason):
        self.__log.info("User ", self.__phonenumber, " disconnected because of reason: ", reason)