#!/usr/bin/env python

import logging
import time
import os

from configuration.configfile import ConfigFile
from connector.whatsapp import WhatsAppConnector
from connector.whatsapp import WhatsAppMessageMetaInfo
from connector.whatsapp import WhatsAppImageUploader

import queue
from messagehandler.messagehandler import MessageHandler
from keywordhandler.echohandler import EchoHandler
from keywordhandler.tumblrhandler import VrijmiboHandler, TettenHandler, BoobsClubHandler, TheLongerViewHandler
from keywordhandler.xkcdhandler import XkcdHandler
from keywordhandler.chhandler import CyanideAndHappinessHandler
from keywordhandler.distributor import ChickDistributor

class JobLock(object):
    def __init__(self):
        self.lock()
        self.__time = time.time()
    def locked(self):
        return self.__lock
    def lock(self):
        self.__lock = True
    def unlock(self):
        self.__lock = False
    def time(self):
        return self.__time

if __name__ == '__main__':
    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename="/var/log/whashose.log")
    
    log.info("Starting up Whashose...")
    
    cfloc = os.path.dirname(os.path.realpath(__file__)) + "/../whashose.config"
    cf = ConfigFile(cfloc)
    
    if not cf.isValid():
        log.error("Invalid configuration file.")
        exit(1)
    
    wac = WhatsAppConnector(cf.phonenumber, cf.password)
    wac.connect()
    
    queue = queue.Queue()
    mh = MessageHandler(queue)

    # Initialisation of the handlers we think are interesting 
    EchoHandler(mh)
    VrijmiboHandler(mh)
    TettenHandler(mh)
    BoobsClubHandler(mh)
    TheLongerViewHandler(mh)
    XkcdHandler(mh)
    CyanideAndHappinessHandler(mh)
    ChickDistributor(mh)
    
    def test(messageId, jid, messageContent, timestamp, wantsReceipt, pushName, isBroadCast):
        log.debug("Received a message from " + jid + " @ " + str(timestamp) + " (" + pushName + ")")
        log.debug("Content: " + messageContent)
        
        meta = WhatsAppMessageMetaInfo(mid=messageId, \
                                       author=jid, \
                                       destination=jid, \
                                       message=messageContent, \
                                       timestamp=timestamp, \
                                       wants_receipt=wantsReceipt, \
                                       pushname=pushName, \
                                       is_broadcast=isBroadCast)
        
        if wantsReceipt:
            wac.methodInterface.call("message_ack", (jid, messageId))
        if isBroadCast:
            return
        mh.handle(meta, messageContent)
        
    def subjecttest(message_id, jid, author, subject, timestamp, receipt_requested):
        log.debug("Group subject received (" + str(subject) + ") from " + str(jid) + " @ " + str(timestamp) + "(" + str(author) + ")")
        
        # Send a help message when we join a group
        if receipt_requested:
            wac.methodInterface.call("message_ack", (jid, message_id))
            
        def subject_message_sent(a, b):
            wac.signalInterface.unregisterListener("receipt_messageSent", subject_message_sent)
            
        wac.signalInterface.registerListener("receipt_messageSent", subject_message_sent)
        wac.methodInterface.call("message_send", (jid, "Hi, I'm whashose. Send a message starting with '@ help' for an explanation on what I can do."))
        
    def grouptest(messageId, jid, author, content, timestamp, wantsReceipt, pushName):
        log.debug("Received a group message from " + author + " @ " + str(timestamp) + " (" + pushName + ") in group " + jid)
        log.debug("Content: " + content)
        
        meta = WhatsAppMessageMetaInfo(mid=messageId, \
                                       author=author, \
                                       destination=jid, \
                                       message=content, \
                                       timestamp=timestamp, \
                                       wants_receipt=wantsReceipt, \
                                       pushname=pushName)
        
        if wantsReceipt:
            wac.methodInterface.call("message_ack", (jid, messageId))
        mh.handle(meta, content)
    
    wac.signalInterface.registerListener("message_received", test)
    wac.signalInterface.registerListener("group_messageReceived", grouptest)
    
    # wac.signalInterface.registerListener("group_subjectReceived", wac.ack_incoming_subject_received)
    wac.signalInterface.registerListener("group_subjectReceived", subjecttest)
    
    wac.signalInterface.registerListener("notification_contactProfilePictureUpdated", wac.ack_incoming_notification_contact_profile_picture_updated)
    wac.signalInterface.registerListener("notification_groupParticipantAdded", wac.ack_incoming_notification_group_participant_added)
    wac.signalInterface.registerListener("notification_groupParticipantRemoved", wac.ack_incoming_notification_group_participant_removed)
    wac.signalInterface.registerListener("notification_groupPictureUpdated", wac.ack_incoming_notification_group_picture_updated)
    wac.signalInterface.registerListener("image_received", wac.ack_incoming_media_image_received)
    wac.signalInterface.registerListener("video_received", wac.ack_incoming_media_video_received)
    wac.signalInterface.registerListener("audio_received", wac.ack_incoming_media_audio_received)
    wac.signalInterface.registerListener("location_received", wac.ack_incoming_media_location_received)
    wac.signalInterface.registerListener("vcard_received", wac.ack_incoming_media_vcard_received)
    wac.signalInterface.registerListener("group_imageReceived", wac.ack_incoming_media_group_image_received)
    wac.signalInterface.registerListener("group_videoReceived", wac.ack_incoming_media_group_video_received)
    wac.signalInterface.registerListener("group_audioReceived", wac.ack_incoming_media_group_audio_received)
    wac.signalInterface.registerListener("group_locationReceived", wac.ack_incoming_media_group_location_received)
    wac.signalInterface.registerListener("group_vcardReceived", wac.ack_incoming_media_group_vcard_received)    
    
    wac.ready()
    
    try:
        while True:
            m = queue.get()
            lock = JobLock()
            jid = m.source_info().destination
            x = m.response().image
            # In case of a text message:
            if m.response().string is not None:
                response = m.response().string
                def receipt_message_sent(a, b):
                    wac.signalInterface.unregisterListener("receipt_messageSent", receipt_message_sent)
                    lock.unlock()
                wac.signalInterface.registerListener("receipt_messageSent", receipt_message_sent)
                wac.methodInterface.call("message_send", (jid, response))
            # In case of an image
            elif m.response().image is not None:
                imgfp = m.response().image
                im_up = WhatsAppImageUploader(m.source_info().author, jid, imgfp, wac)
                im_up.upload(lock)
            else:
                msg = "ERROR: Message is not provided with a valid response..."
                log.debug(msg)
                raise Exception(msg)
                
            while lock.locked():
                if (time.time() - lock.time()) > 30:
                    
                    log.error("ERROR: This probably is a race condition, we are still waiting on the lock. Exitting...")
                    wac.disconnect("We probably detected a race condition")
                    time.sleep(2)
                    exit(1);
                    
                log.debug("Waiting for lock...")
                time.sleep(1)
    except KeyboardInterrupt:
        log.info("Ctrl-C catched -- exitting...")
        wac.disconnect("Ctrl-c pressed")
        time.sleep(3)
        
    exit(0)
