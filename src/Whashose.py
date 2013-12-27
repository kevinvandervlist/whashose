#!/usr/bin/env python

import logging
import time
import os

from configuration.configfile import ConfigFile
from connector.whatsapp import WhatsAppConnector

if __name__ == '__main__':
    log = logging.getLogger(__name__)
    log.info("Starting up Whashose...")
    
    cfloc = os.path.dirname(os.path.realpath(__file__)) + "/../whashose.config"
    cf = ConfigFile(cfloc)
    
    if not cf.isValid():
        log.error("Invalid configuration file.")
        exit(1)
    
    wac = WhatsAppConnector(cf.phonenumber, cf.password)
    wac.connect()
    wac.ready()
    
    time.sleep(2)
    log.info("Stopping...")
    wac.disconnect("End of program")
    time.sleep(1)
    
    #try:
    #    while True:
    #        time.sleep(5)
    #except KeyboardInterrupt:
    #    log.info("Ctrl-C catched -- exitting...")
    #    wac.disconnect("Ctrl-c pressed")
    #    time.sleep(3)
        
    exit(0)