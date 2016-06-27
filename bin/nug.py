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

# def diff(first, second):
#     second = set(second)
#     return [item for item in first if item not in second]


passwd_entrys = getfileAsListOfLists(nismap_item_path,":")
user_id_list_raw = column(passwd_entrys,2)

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

# print "-------------------------------------------------------"
# if len(user_id_list_raw) != len(user_id_set):
#     print("User IDs are not uniq !!")
#     print("number 0f read IDs = {}".format(len(user_id_list_raw)))
#     print("number 0f uniq IDs = {}".format(len(user_id_set)))
#     double_ids = diff(user_id_list_raw,user_id_set)
#     print("double_ids = {}".format(double_ids))
# else:
#     print("User IDs are OK")


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