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

passwd_entrys = getfileAsListOfLists(nismap_item_path,":")
user_id_list_raw = column(passwd_entrys,2)
user_id_set = set(user_id_list_raw)


print user_id_list_raw

print "-------------------------------------------------------"
if len(user_id_list_raw) != len(user_id_set):
    print("User IDs are not uniq !!")
    print("number 0f read IDs = {}".format(len(user_id_list_raw)))
    print("number 0f uniq IDs = {}".format(len(user_id_set)))
    for id in user_id_list_raw:
        print("{}".format(id))
else:
    print("User IDs are OK")
