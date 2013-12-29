#!/usr/bin/python

import base64
import time
import datetime
import hashlib
import os
from PIL import Image
from io import BytesIO

from Yowsup.connectionmanager import YowsupConnectionManager



from Yowsup.Media.uploader import MediaUploader


class ImageUploader(object):
    def __init__(self, from_jid, to_jid, img_path, methods_interface):
        self.from_jid = from_jid
        self.to_jid = to_jid
        self.img_path = img_path
        self.img_name = os.path.basename(img_path)
        self.methods_interface = methods_interface
        self.mtype = "image"
        self.uploader = MediaUploader(from_jid, to_jid, self.on_upload_success, self.on_error, self.on_progress_updated)

    def upload(self):
        sha256 = hashlib.sha256()
        fp = open(self.img_path, 'rb')

        try:
            im = Image.open(self.img_path)
            im.thumbnail((128, 128), Image.ANTIALIAS)
            output = BytesIO()
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
        print("Trying to deliver message for url: ", url)
        self.methods_interface.call("message_imageSend", (self.to_jid, url, self.img_name, str(self.size), self.b64preview))

    def upload_request_success(self, _hash, url, resume_from):
        print("\tUpload request succes:")
        print(_hash)
        print(url)
        print(resume_from)
        self.uploader.upload(self.img_path, url)

    def upload_request_failed(self, _hash):
        print("\tUpload request failed:")
        print(_hash)

    def upload_request_duplicate(self, _hash, url):
        print("\tDuplicate request: ")
        print(_hash)
        print(url)
        self.deliverMessage(url)

    def on_upload_success(self, url):
        self.deliverMessage(url)

    def on_error(self):
        print("\tFailed to upload")

    def on_progress_updated(self, progress):
        print("\tProgress: " + str(progress))

class ProfilePictureClient:
    
    def __init__(self):
        y = YowsupConnectionManager()
        y.setAutoPong(True)

        self.signalsInterface = y.getSignalsInterface()
        self.methodsInterface = y.getMethodsInterface()


        self.signalsInterface.registerListener("auth_fail", self.onAuthFailed)
        self.signalsInterface.registerListener("auth_success", self.onAuthSuccess)
        self.signalsInterface.registerListener("disconnected", self.onDisconnected)
        self.signalsInterface.registerListener("message_received", self.onMessageReceived)
        self.signalsInterface.registerListener("profile_setPictureSuccess", self.onSetPictureSuccess)

    def doLogin(self, user="", pw=""):
        password = base64.b64decode(bytes(pw.encode('utf-8')))
        self.methodsInterface.call("auth_login", (user, password))

    def disconnect(self, reason):
        self.methodsInterface.call("disconnect", (reason, ))

    def onAuthSuccess(self, username):
        print("Logged in with: " + username)

        self.methodsInterface.call("ready")
        # Set a profile picture
        #self.methodsInterface.call("profile_setPicture", (("/home/kevin/src/yowsup/src/avatar.jpg", )))
        # upload a profile picture
        image = "/tmp/t.jpg"
        from_jid="31649791025@s.whatsapp.net"
        to_jid="31643429955@s.whatsapp.net"
        
        im_up = ImageUploader(from_jid, to_jid, image, self.methodsInterface)

        self.signalsInterface.registerListener("media_uploadRequestSuccess", im_up.upload_request_success)
        self.signalsInterface.registerListener("media_uploadRequestFailed", im_up.upload_request_failed)
        self.signalsInterface.registerListener("media_uploadRequestDuplicate", im_up.upload_request_duplicate)

        im_up.upload()

    def onSetPictureSuccess(self, bar):
        print("Set picture succesfully!")
        print(bar)

    def onAuthFailed(self, username, err):
        print("Auth Failed!")

    def onDisconnected(self, reason):
        print("Disconnected because %s" %reason)

    def onMessageReceived(self, messageId, jid, messageContent, timestamp, wantsReceipt, pushName, isBroadCast):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        print("%s [%s]:\n\nReceived the following text:\n%s\n\n"%(jid, formattedDate, messageContent))
        
        if wantsReceipt:
            self.methodsInterface.call("message_ack", (jid, messageId))
    

p = ProfilePictureClient()
p.doLogin("31649791025", "Zb4JwG5MQO6EZBffFpS53PuWVNM=")

# listeners = [component1, component2, component3]
# eventqueue.add(InitEvent())
# while True:
#     event = eventqueue.pop()
#     for listener in listeners:
#         listener.handle_event(event)

time.sleep(5)
p.disconnect("End")
time.sleep(1)

# try:
#     while True:
#         print("Event loop iteration.")
#         time.sleep(5)
# except KeyboardInterrupt:
#     print("Exitting...")
#     p.disconnect("Ctrl-c")
#     time.sleep(1)
