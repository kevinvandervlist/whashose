'''
Created on 26 Dec 2013

@author: kevin
'''

import logging
import base64

from Yowsup.connectionmanager import YowsupConnectionManager

class WhatsAppMessageMetaInfo(object):
    '''
    Value object to retain some meta information on a message
    '''
    def __init__(self, mid, author, destination, message, timestamp, wants_receipt, pushname, is_broadcast=False):
        self.mid = mid
        self.author = author
        self.destination = destination
        self.message = message
        self.timestamp = timestamp
        self.wants_receipt = wants_receipt
        self.pushname = pushname
        self.is_broadcast = is_broadcast

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
        self.__log.info("User ", self.__phonenumber, " will try to disconnect because of reason: " + reason)
        self.methodInterface.call("disconnect", (reason, ))
    
    def __on_auth_success(self, username):
        self.__log.info("User " + username + " successfully logged in.")
        
    def __on_auth_failed(self, username, err):
        self.__log.error("Can't login " + username + " because of error: " + err)
        
    def __on_disconnected(self, reason):
        self.__log.info("User " + self.__phonenumber + " disconnected because of reason: " + reason)
        
    # Scaffolding for acks
    def __ack(self, message_id, jid, receipt_requested):
        '''
        signalInterface.registerListener("message_received", ack_incoming_message)
        signalInterface.registerListener("group_messageReceived", ack_incoming_group_message)
        signalInterface.registerListener("group_subjectReceived", ack_incoming_subject_received)
        signalInterface.registerListener("notification_contactProfilePictureUpdated", ack_incoming_notification_contact_profile_picture_updated)
        signalInterface.registerListener("notification_groupParticipantAdded", ack_incoming_notification_group_participant_added)
        signalInterface.registerListener("notification_groupParticipantRemoved", ack_incoming_notification_group_participant_removed)
        signalInterface.registerListener("notification_groupPictureUpdated", ack_incoming_notification_group_picture_updated)
        signalInterface.registerListener("image_received", ack_incoming_media_image_received)
        signalInterface.registerListener("video_received", ack_incoming_media_video_received)
        signalInterface.registerListener("audio_received", ack_incoming_media_audio_received)
        signalInterface.registerListener("location_received", ack_incoming_media_location_received)
        signalInterface.registerListener("vcard_received", ack_incoming_media_vcard_received)
        signalInterface.registerListener("group_imageReceived", ack_incoming_media_group_image_received)
        signalInterface.registerListener("group_videoReceived", ack_incoming_media_group_video_received)
        signalInterface.registerListener("group_audioReceived", ack_incoming_media_group_audio_received)
        signalInterface.registerListener("group_locationReceived", ack_incoming_media_group_location_received)
        signalInterface.registerListener("group_vcardReceived", ack_incoming_media_group_vcard_received)
        '''
        if receipt_requested:
            self.methodInterface.call("message_ack", (jid, message_id))
        
    def ack_incoming_message(self, message_id, jid, message_content, timestamp, receipt_requested, push_name, is_broadcast):
        self.__ack(message_id, jid, receipt_requested)
        
    def ack_incoming_group_message(self, message_id, jid, author, content, timestamp, receipt_requested, push_name):
        self.__ack(message_id, jid, receipt_requested)
        
    def ack_incoming_subject_received(self, message_id, jid, author, subject, timestamp, receipt_requested):
        self.__ack(message_id, jid, receipt_requested)
        
    def ack_incoming_notification_contact_profile_picture_updated(self, jid, timestamp, message_id, receipt_requested):
        self.__ack(message_id, jid, receipt_requested)
        
    def ack_incoming_notification_group_participant_added(self, group_jid, jid, author, timestamp, message_id, receipt_requested):
        self.__ack(message_id, jid, receipt_requested)

    def ack_incoming_notification_group_participant_removed(self, group_jid, jid, author, timestamp, message_id, receipt_requested):
        self.__ack(message_id, jid, receipt_requested)
        
    def ack_incoming_notification_group_picture_updated(self, jid, author, timestamp, message_id, receipt_requested):
        self.__ack(message_id, jid, receipt_requested)
        
    def ack_incoming_media_image_received(self, message_id, jid, preview, url, size, receipt_requested, is_broadcast):
        self.__ack(message_id, jid, receipt_requested)

    def ack_incoming_media_video_received(self, message_id, jid, preview, url, size, receipt_requested, is_broadcast):
        self.__ack(message_id, jid, receipt_requested)

    def ack_incoming_media_audio_received(self, message_id, jid, url, size, receipt_requested, is_broadcast):
        self.__ack(message_id, jid, receipt_requested)
        
    def ack_incoming_media_location_received(self, message_id, jid, name, preview, lattitude, longtitude, receipt_requested, is_broadcast):
        self.__ack(message_id, jid, receipt_requested)

    def ack_incoming_media_vcard_received(self, message_id, jid, name, data, receipt_requested, is_broadcast):
        self.__ack(message_id, jid, receipt_requested)
        
    def ack_incoming_media_group_image_received(self, message_id, jid, author, preview, url, size, receipt_requested):
        self.__ack(message_id, jid, receipt_requested)

    def ack_incoming_media_group_video_received(self, message_id, jid, author, preview, url, size, receipt_requested):
        self.__ack(message_id, jid, receipt_requested)

    def ack_incoming_media_group_audio_received(self, message_id, jid, author, url, size, receipt_requested):
        self.__ack(message_id, jid, receipt_requested)
        
    def ack_incoming_media_group_location_received(self, message_id, jid, author, name, preview, lattitude, longtitude, receipt_requested):
        self.__ack(message_id, jid, receipt_requested)

    def ack_incoming_media_group_vcard_received(self, message_id, jid, author, name, data, receipt_requested):
        self.__ack(message_id, jid, receipt_requested)