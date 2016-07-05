#!/usr/bin/env python

import sys
from Tkinter import *
import tkFont
from PIL import Image, ImageTk
import ScrolledText
import subprocess as sub
import os,time,datetime
import re
from collections import defaultdict

pydir =  os.path.dirname(os.path.abspath(__file__))
basedir = os.path.dirname(pydir)
imagedir = os.path.join(basedir, "images")
animdir = os.path.join(imagedir, "animated_gifs")
logo_filename = 'dfs.gif'
logo_file = os.path.join(imagedir, logo_filename)
libdir = os.path.join(basedir,"lib")
sys.path.append(libdir)

# nismap_basedir = os.path.join(os.path.sep,"srv","inst","cfg","nis")
# nis_domain = "se"
# nismap_dir = os.path.join(nismap_basedir,nis_domain)


from lib.user_manager_model import *

version = "0.7"
main_window_title = " OPT User Manager " + version + " (unregistered) "
about = main_window_title + "(c) Peter Krauspe DFS 7/2016"

print("logo_file={}".format(logo_file))

class UserManagerGUI(Frame):
    def __init__(self, root=None):
        # MAIN FRAME
        Frame.__init__(self, root)
        print "screenwidth ", root.winfo_screenwidth()
        print "screenheight ", root.winfo_screenheight()
        self.max_app_width = root.winfo_screenwidth()
        self.max_app_height = int(root.winfo_screenheight()*0.9)
        # Limit root window size
        root.maxsize(width=self.max_app_width,height=self.max_app_height)
        self.parent = root # get a reference to change atts of the root window (like title etc)
        self.frame = Frame(root)
        self.frame.grid(row=0,column=1)
        self.logo = PhotoImage(file=logo_file)
        Label(self.frame, image=self.logo, relief=GROOVE).grid(row=0,column=1,sticky="E")

        userManagemnetModel = UserManagement()
        fileutil = FileUtilImpl()
        importer = PasswdImporter(userManagemnetModel, fileutil)

        passwdFileImported = importer.importFromPasswdFile("local")
        validator = Validator(userManagemnetModel)


        if(passwdFileImported):

            # print userManagemnetModel
            r = 1
            # simple gui to test model
            for user in userManagemnetModel.userlist:
                c = 0
                for item in (user.name, user.uid, user.gid, user.fullname, user.location, user.phone, user.homedir, user.shell, user.ugroup, user.extcomment, user.UIDisUniq):
                    Label(self.frame, text=item).grid(row=r, column=c, sticky="w")
                    c += 1
                r += 1
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

if __name__ == "__main__":
    root = Tk()
    # root.geometry("800x600")  # mal testen !!
    root.title(main_window_title)
    main = UserManagerGUI(root)
    #main.grid(row=0,column=0)
    main.grid()
    root.mainloop()


