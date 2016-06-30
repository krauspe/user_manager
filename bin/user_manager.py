#!usr/bin/env python
#
# Manage NIS Users
#
# (c) Peter Krauspe 6/2016
#
import os
#import socket
from collections import defaultdict
#import argparse
import json
#import hjson
from prettyprint import pp
#import re
#from sys import argv,exit


#bondi011:ntnoV/yui2Cs:2031:105:Dirk Bonekaemper,1.0xy,06103/707-5728:/export/home/bondi011:/bin/bash
#tuean030:M.EkllMjkljeXJc:2032:105:Andreas Tuerk,1.014,06103/707-57xx:/export/home/tuean030:/bin/bash
#krape030:10UNl890njkXKss:2033:105:Peter Krauspe,1.0xx,06103/707-5739:/export/home/krape030:/bin/bash


pydir =  os.path.dirname(os.path.abspath(__file__))
basedir = os.path.dirname(pydir)
bindir  = os.path.join(basedir,"bin")
vardir  = os.path.join(basedir,"var")
nismap_basedir = os.path.join(os.path.sep,"srv","inst","cfg","nis")
nis_domain = "se"
nismap_dir = os.path.join(nismap_basedir,nis_domain)


def getfileAsListOfLists(file,separator):
    listOfLists = []
    if os.path.exists(file):
        with open(file) as f:
            Lines = f.read().splitlines()

        if len(Lines) < 0:
            print ("WARNING: {%s} is empty or has no valid lines !!" , file)
            return []
        else:
            listOfLists  = [line.split(separator) for line in Lines if not line.startswith('#')]
            return listOfLists
    else:
        print ("WARNING: {%s} doesn't exist !!" , file)
        return []


def column(table,i):
    return [row[i] for row in table]


class PasswdImporter(object):

    #pwdlines = defaultdict(lambda:'')

    def __init (self, model):
        self.userManagementModel = model

    def importFromPasswdFile(self, filename, type):
        if type == "local":
            file_path = os.path.join(nismap_dir,"passwd")
            pwdlines = getfileAsListOfLists(file_path,":")
        else:
            print("currently only type 'local' is supported!")
            return False
        if len(pwdlines) == 0:
            return False

        # iterate over pwd lines
        for name, pwd, gid, uid, pwdcomment, homedir, shell in pwdlines:
            fullname,location,phone = pwdcomment.split(',')
            user = User(name=name, pwd=pwd, gid=gid, uid=uid, fullname=fullname, location=location, phone=phone, homedir=homedir, shell=shell, ugroup="", extcomment="", UIDisUniq=True)
            self.userManagementModel.addUser(user)

class Validator(object):
    def __init (self, model):
        self.userManagementModel = model

    def getDuplicateUIDs(self):
        seen_set = set()
        return set(x for x in self.userManagementModel.getUIDs() if x in seen_set or seen_set.add(x))

    def checkUID(self):
        duplicates = self.getDuplicateUIDs()
        for uid in duplicates:
            usersWithDuplicateUid = self.userManagementModel.getAllUsersWithUid(uid)
            for usr in usersWithDuplicateUid:
                usr.UIDisUniq = False
        return len(duplicates) == 0

class UserManagement(object):
    """User Database"""

    def __init__(self):
        """Constructor"""
        self.userlist = []

    def addUser(self, user):
        """Add User"""
        self.userlist.append(user)

        return id

    def query(self, User):
        """Query User"""
        pass


    def deleteUser(self, user):
        """Delete User"""
        self.userlist.remove(user)

    def getAllUsersWithUid(self, uid):
        """List Users"""
        userList = []
        for usr in self.userlist:
            if(usr.uid == uid):
                userList.append(usr)
        return userList

    def getUIDs(self):
        uidList = []
        for usr in self.userlist:
            uidList.append(usr.uid)
        return uidList



class User(object):
    idCounter = 0
    def __init__(self, name="", pwd="", gid=-1, uid=-1, fullname="", location="", phone="", homedir="", shell="", ugroup="", extcomment="", UIDisUniq=True):
        """Constructor"""
        self.ID = User.idCounter
        User.idCounter += 1
        self.name = name
        self.pwd  = pwd
        self.gid  = gid
        self.uid  = uid
        self.fullname = fullname
        self.location = location
        self.phone = phone
        self.homedir = homedir
        self.shell = shell
        self.group = ugroup
        self.extcomment = extcomment
        self.UIDisUniq = UIDisUniq

    def isValid(self):
        return self.uid >= 0 and self.gid >= 0 and self.name != ""  ##TODO: complete...

    def getPwdLine(self):
        PwdLineItems = [
            self.name,
            self.pwd ,
            self.gid ,
            self.uid ,
            ",".join(self.fullname , self.location , self.phone),
            self.homedir,
            self.shell,
        ]
        return PwdLineItems.join(":")



# main

# instanciate model

userManagemnetModel = UserManagement()
importer = PasswdImporter(userManagemnetModel)

rc = importer.importFromPasswdFile("passwd", "local")

if(rc):
    print userManagemnetModel
else:
    print "something wrong with passwd import"


# unique_ids_set = user_id_list_raw - list(seen_set)

#print "duplicate_ids_set:"
#for id in duplicate_ids_set:
#    print id

# print "unique_ids_set:"
# for id in unique_ids_set:
#     print id
#
# print user_id_list_raw



