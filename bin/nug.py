#!","usr","bin","env python
#
# Manage NIS Users
#
# (c) Peter Krauspe 6/2016
#
import os
#import socket
#import collections
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
nismap_item = "passwd"
nismap_item_path = os.path.join(nismap_dir,nismap_item)

print ("nismap_item_path ={}".format(nismap_item_path))


def getfileAsListOfLists(file,separator):
    ListOfLists = []
    if os.path.exists(file):
        with open(file) as f:
            Lines = f.read().splitlines()

        if len(Lines) < 0:
            print "WARNING: %s is empty or has no valid lines !!" % file

        ListOfLists  = [line.split(separator) for line in Lines if not line.startswith('#')]
        return ListOfLists
    else:
        print "WARNING: %s doesn't exist !!" % file
        return []

def column(table,i):
    return [row[i] for row in table]


class Users(object):
    """User Database"""

    def __init__(self):
        """Constructor"""
        self.passwd_entrys_lol = getfileAsListOfLists(nismap_item_path,":")
        self.Name = ""
        self.Pwd  = ""
        self.UID  = 0
        self.GUI  = 0
        self.FullName = ""
        self.Location = "1.000"
        self.Phone = ""
        self.Comment = ""
        self.HomeDir = ""
        self.Shell = os.path.join("bin","bash")


    def add(self, User):
        """Add User"""

        return id

    def query(self, User):
        """Query User"""
        pass


    def delete(self, User):
        """Delete User"""
        pass

    def getUserList(self):
        """List Users"""
        pass

    def getIdList(self):
        return column(self.passwd_entrys_lol,2)

class User(self):
    def __init__(self,id):
        """Constructor"""
        pass





seen_set = set()
duplicate_ids_set = set(x for x in user_id_list_raw if x in seen_set or seen_set.add(x))
# unique_ids_set = user_id_list_raw - list(seen_set)

print "duplicate_ids_set:"
for id in duplicate_ids_set:
    print id

# print "unique_ids_set:"
# for id in unique_ids_set:
#     print id
#
# print user_id_list_raw



# NEUE ideen

## Very simple and quick way of finding dupes with one iteration in Python is:
#
 # testList = ['red', 'blue', 'red', 'green', 'blue', 'blue']
#
# testListDict = {}
#
# for item in testList:
#   try:
#     testListDict[item] += 1
#   except:
#     testListDict[item] = 1
#
# print testListDict
#
# Output will be as follows:
#
# >>> print testListDict
# {'blue': 3, 'green': 1, 'red': 2}