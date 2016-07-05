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
import unittest


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
            print ("WARNING: \"{}\" is empty or has no valid lines !!" , file)
            return []
        else:
            listOfLists  = [line.split(separator) for line in Lines if not line.startswith('#')]
            return listOfLists
    else:
        print ("WARNING: \"{}\" doesn't exist !!" , file)
        return []


class FileUtil(object):
    def getFileAsListOfLists(self, file,separator):
        return 1

class FileUtilImpl(FileUtil):
    def getFileAsListOfLists(self, file,separator):
        if os.path.exists(file):
            with open(file) as f:
                Lines = f.read().splitlines()

            if len(Lines) < 0:
                print ("WARNING: \"{}\" is empty or has no valid lines !!", file)
                return []
            else:
                listOfLists = [line.split(separator) for line in Lines if not line.startswith('#')]
                return listOfLists
        else:
            print ("WARNING: \"{}\" doesn't exist !!", file)
            return []

class FileUtilMock(FileUtil):
    def __init__(self, listOflines):
        self.lol = listOflines

    def getFileAsListOfLists(self, file,separator):
        return self.lol


def column(table,i):
    return [row[i] for row in table]


class PasswdImporter(object):

    def __init__ (self, model, fileutil):
        self.userManagementModel = model
        self.fileutil = fileutil

    def importFromPasswdFile(self, type):
        if type == "local":
            file_path = os.path.join(nismap_dir,"passwd")
            pwdlines = self.fileutil.getFileAsListOfLists(file_path,":")
        else:
            print("currently only type 'local' is supported!")
            return False
        if len(pwdlines) == 0:
            return False

        # iterate over pwd lines, parse pwdcomment
        for name, pwd, uid, gid, pwdcomment, homedir, shell in pwdlines:

            comment_items = pwdcomment.split(',')
            fullname = ""; location = ""; phone = ""

            try : fullname = comment_items[0]
            except IndexError: pass

            try :
                if comment_items[1][:2].isdigit():
                    phone = comment_items[1]
                else:
                    location = comment_items[1]
            except IndexError: pass

            try :
                if comment_items[2][:1].isdigit():
                    phone = comment_items[2]
            except IndexError: pass

            user = User(name=name, pwd=pwd, uid=int(uid), gid=int(gid), fullname=fullname, location=location, phone=phone, homedir=homedir, shell=shell, ugroup="", extcomment="", UIDisUniq=True)
            self.userManagementModel.addUser(user)

        return True

class Validator(object):
    def __init__(self, model):
        self.userManagementModel = model

    def getDuplicateUIDs(self):
        seen_set = set()
        return set(x for x in self.userManagementModel.getUIDs() if x in seen_set or seen_set.add(x))

    def checkUidsUniq(self):
        duplicates = self.getDuplicateUIDs()
        for uid in duplicates:
            #print("Validator.checkUidsUniq(): Found dup uid {}".format(uid))
            usersWithDuplicateUid = self.userManagementModel.getAllUsersWithUid(uid)
            for usr in usersWithDuplicateUid:
                #print "     setting UIDisUniq to False"
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
        userlist = []
        for usr in self.userlist:
            if(usr.uid == uid):
                userlist.append(usr)
        return userlist

    def getUIDs(self):
        uidList = []
        for usr in self.userlist:
            uidList.append(usr.uid)
        return uidList



class User(object):
    idCounter = 0
    def __init__(self, name="", pwd="", uid=-1, gid=-1, fullname="", location="", phone="", homedir="", shell="", ugroup="", extcomment="", UIDisUniq=True):
        """Constructor"""
        self.ID = User.idCounter
        User.idCounter += 1
        self.name = name
        self.pwd  = pwd
        self.uid  = uid
        self.gid  = gid
        self.fullname = fullname
        self.location = location
        self.phone = phone
        self.homedir = homedir
        self.shell = shell
        self.ugroup = ugroup
        self.extcomment = extcomment
        self.UIDisUniq = UIDisUniq

    def isValid(self):
        return self.uid >= 0 and self.gid >= 0 and self.name != ""  ##TODO: complete...

    def getUserInfoLine(self):
        dataLineItems = []
        return 'name=\"{}\"  pwd=\"{}\", uid=\"{}\", gid=\"{}\", fullname=\"{}\", location=\"{}\", phone=\"{}\", homedir=\"{}\", shell=\"{}\", ugroup=\"{}\", extcomment=\"{}\", UIDisUniq=\"{}\" '.format(
                self.name, self.pwd, self.uid, self.gid, self.fullname, self.location, self.phone, self.homedir, self.shell, self.ugroup, self.extcomment, self.UIDisUniq)

    def getUserInfoLine2(self):
        lineItems = [
        str(self.ID),
        self.name,
        self.pwd ,
        str(self.uid) ,
        str(self.gid) ,
        self.fullname,
        self.location,
        self.phone,
        self.homedir,
        self.shell,
        self.ugroup,
        self.extcomment,
        str(self.UIDisUniq)
        ]
        return " | ".join(lineItems)

    def getPwdLine(self):
        pwdLineItems = [
            self.name,
            self.pwd ,
            str(self.gid) ,
            str(self.uid) ,
            ",".join([self.fullname , self.location , self.phone]),
            self.homedir,
            self.shell,
        ]
        return ":".join(pwdLineItems)


class TestUserManagement(unittest.TestCase):
    def testSimpel(self):
        userManagemnetModel = UserManagement()

        pwdTestLines = [
                ["bondi011","ntnoV/yui2Cs","2031","105","Dirk Bonekaemper,1.0xy,06103/707-5728","/export/home/bondi011","/bin/bash"],
                ["tuean030","M.EkllMjkljeXJc","2032","105","Andreas Tuerk,1.014,06103/707-57xx","/export/home/tuean030","/bin/bash"],
                ["krape030","10UNl890njkXKss","2031","105","Peter Krauspe,1.0xx,06103/707-5739","/export/home/krape030","/bin/bash"]
            ]

        fileutil = FileUtilMock(pwdTestLines)
        importer = PasswdImporter(userManagemnetModel, fileutil)

        passwdFileImported = importer.importFromPasswdFile("local")
        validator = Validator(userManagemnetModel)


        if(passwdFileImported):

            self.assertEqual(len(pwdTestLines), len(userManagemnetModel.userlist))
            # print userManagemnetModel
            for user in userManagemnetModel.userlist:
                print user.getPwdLine()

            print "\n-------------------------------------------------\n"

            for user in userManagemnetModel.userlist:
                print user.getUserInfoLine()

            print "\n-------------------------------------------------\n"

            if not validator.checkUidsUniq():
                print "\nFollowing Users have NO UNIQ IDs:\n"
                for user in userManagemnetModel.userlist:
                    if not user.UIDisUniq:
                        print user.getUserInfoLine()

        else:
            print "something wrong with passwd import"


if __name__ == '__main__':
    unittest.main()


