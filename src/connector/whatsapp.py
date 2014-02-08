'''
Created on 26 Dec 2013

@author: kevin
'''

import logging
import base64

import hashlib
import os
import time
from PIL import Image
from io import BytesIO
from Yowsup.connectionmanager import YowsupConnectionManager
from Yowsup.Media.uploader import MediaUploader

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
        
    def __str__(self):
        return ("MessageID:" + str(self.mid) + 
                ", Author: " + str(self.author) + 
                ", Destination: " + str(self.destination) +
                ", Message: " + str(self.message) +
                ", timestamp: " + str(self.timestamp) +
                ", pushname: " + str(self.pushname))

class WhatsAppImageUploader(object):
    def __init__(self, from_jid, to_jid, img_fp, wac):
        self.__log = logging.getLogger(__name__)
        self.from_jid = from_jid
        self.to_jid = to_jid
        self.img_fp = img_fp
        self.img_path = img_fp.name
        self.img_name = os.path.basename(img_fp.name)
        self.methods_interface = wac.methodInterface
        self.fp_dict = dict()
        self.message_id = None
        self.wac = wac
        
        wac.signalInterface.registerListener("media_uploadRequestSuccess", self.upload_request_success)
        wac.signalInterface.registerListener("media_uploadRequestFailed", self.upload_request_failed)
        wac.signalInterface.registerListener("media_uploadRequestDuplicate", self.upload_request_duplicate)
        wac.signalInterface.registerListener("receipt_messageSent", self.receipt_message_sent)
        
        self.mtype = "image"
        self.uploader = MediaUploader(from_jid, to_jid, self.on_upload_success, self.on_error, self.on_progress_updated)
        
    def cleanup(self):
        self.__log.error("6) Cleanup for " + self.img_path)
        self.img_fp.close()
        os.remove(self.img_path)
        self.wac.signalInterface.unregisterListener("media_uploadRequestSuccess", self.upload_request_success)
        self.wac.signalInterface.unregisterListener("media_uploadRequestFailed", self.upload_request_failed)
        self.wac.signalInterface.unregisterListener("media_uploadRequestDuplicate", self.upload_request_duplicate)
        self.wac.signalInterface.unregisterListener("receipt_messageSent", self.receipt_message_sent)
        self.lock.unlock()
        self.__log.debug("7) Lock: " + str(self.lock.locked()))
        
    def upload(self, lock):
        self.__log.debug("1) calling upload() for " + self.img_path)
        self.lock = lock
        
        sha256 = hashlib.sha256()
        fp = open(self.img_path, 'rb')

        try:
            im = Image.open(self.img_path)
            im.thumbnail((128, 128), Image.ANTIALIAS)
            output = BytesIO()
            if im.mode != "RGB":
                im.convert("RGB")
            im.save(output, format='JPEG')
            output.seek(0)
            self.b64preview = base64.b64encode(output.read())
            
            sha256.update(fp.read())
            _hash = base64.b64encode(sha256.digest())
            self.size = os.path.getsize(self.img_path)
            self.methods_interface.call("media_requestUpload", (_hash, self.mtype, self.size))
        finally:
            fp.close()
            
    def deliverMessage(self, url):
        self.__log.debug("4) Trying to deliver message for url:" + url)
        message_id = self.methods_interface.call("message_imageSend", (self.to_jid, url, self.img_name, str(self.size), self.b64preview))
        
        #self.img_fp.close()
        if self.message_id is not None:
            self.__log.error("4) Invalid message ID: It is already set: " + self.message_id + "; new: " + message_id)
        self.message_id = message_id
        
    def receipt_message_sent(self, jid, message_id):
        self.__log.debug("5) receipt_message_sent for message_id: " + message_id)
        
        self.__log.error("5) Closing and removing fP: " + self.img_path)
        self.cleanup()

    def upload_request_success(self, _hash, url, resume_from):
        self.__log.debug("2) Upload request succes for file:" + self.img_path)
        self.__log.debug(_hash)
        self.__log.debug(url)
        self.__log.debug(resume_from)
        self.uploader.upload(self.img_path, url)

    def upload_request_failed(self, _hash):
        self.__log.debug("2) Upload request failed:")
        self.__log.debug(_hash)

    def upload_request_duplicate(self, _hash, url):
        self.__log.debug("2) Duplicate request: ")
        self.__log.debug(_hash)
        self.__log.debug(url)
        self.deliverMessage(url)

    def on_upload_success(self, url):
        self.__log.debug("3) Successful upload: " + url + "(" + self.img_path + ")")
        self.deliverMessage(url)

    def on_error(self):
        self.__log.error("3) Failed to upload, closing file: " + self.img_fp.name)
        self.cleanup()

    def on_progress_updated(self, progress):
        pass

class WhatsAppConnector(object):
    '''
    classdocs
    '''


    def __init__(self, phonenumber=None, password=None, autopong=True, reconnect_on_closed=True):
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
        
        self.__reconnect_on_closed=reconnect_on_closed
        
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
        self.__log.info("User " + self.__phonenumber + " will try to disconnect because of reason: " + reason)
        self.methodInterface.call("disconnect", (reason, ))
    
    def __on_auth_success(self, username):
        self.__log.info("User " + username + " successfully logged in.")
        
    def __on_auth_failed(self, username, err):
        self.__log.error("Can't login " + username + " because of error: " + err)
        
    def __on_disconnected(self, reason):
        self.__log.info("User " + self.__phonenumber + " disconnected because of reason: " + reason)
        # If WhatsApp disconnects us, automatically reestablish the connection
        if reason is "closed" and self.__reconnect_on_closed:
            self.__log.info("Automatically trying to reestablish the connection...")
            self.connect()
            time.sleep(3)
            self.ready()
        
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
        
    def ack_incoming_notification_group_picture_updated(self, jid, author, timestamp, message_id, picture_id, receipt_requested):
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