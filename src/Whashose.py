#!/usr/bin/env python

from configuration.configfile import ConfigFile

if __name__ == '__main__':

    print("Starting up Whashose...")
    cf = ConfigFile("/home/kevin/src/personal/whashose/whashose.config")
    if cf.isValid():
        print(cf.phonenumber)
        print(cf.password)
    else:
        print("Invalid config")
