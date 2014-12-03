#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 13.07.2012

@author: Christian Pollmann
'''
from config import *
import sys,Image,ImageFont,ImageDraw,smtplib
from time import *

def error(mesg):
    smtpserver = smtplib.SMTP(gmail_server,gmail_server_port)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: LED-Anzeige <' + gmail_user + '>\n' + 'Subject: ERROR: Unable to create image! \n'
    msg  = header 
    msg +='\n'+mesg+'\n'
    smtpserver.sendmail(gmail_user, to, msg)
    smtpserver.close()
    sys.exit(mesg)

def newLED(extended=False):
    if not extended:
        return Image.new(imagemode,ledsize,backgroundcolor)
    else:
        return Image.new(imagemode,(ledsize[0]*2,ledsize[1]),backgroundcolor)

def setFont():
    return ImageFont.truetype(fontfile,fontsize)

def setWorkspace(image):
    return ImageDraw.Draw(image)

def writeText(draw,text,cursor):
    position=(cursor,fontheight)
    draw.text(position,text,fontcolor,setFont())
    return setFont().getsize(text)[0]

def addAnd(image,andsymbol,cursor):
    image.paste(andsymbol,(cursor,0))

# wochentagsabhaengige Aenderung der Verschiebung, um Abnutzung der LEDs zu verhindern
def chgfriendsword():
    lt=localtime()
    weekday=strftime("%w", lt)
    friendswd=friendsword
    if weekday=="1":
        friendswd=friendsword+" "
    if weekday=="3":
        friendswd=friendsword+" "
    if weekday=="5":
        friendswd=friendsword+" "
    return friendswd

def generateImage(name,b_addAnd=True):
    TEXT=name
    image=newLED(True)
    draw=setWorkspace(image)
    cursor = 0
    for i in range(0, len(TEXT)):
    	skip=False
    	try:
    		if TEXT[i-1]=="<" and TEXT[i]=="3":
    			skip=True
    		if TEXT[i]=="<" and TEXT[i+1]=="3":
    			skip=True
    			heartsymbol=Image.open(heartpath,"r")
    			addAnd(image,heartsymbol,cursor)
    			cursor+=heartwidth+fontspacing
    	except:
    		pass
    	if not skip:
        	cursor+=writeText(draw,TEXT[i],cursor)+fontspacing
    if b_addAnd:
        cursor+=middlespace
        for BST in friendsword:
            cursor+=writeText(draw,BST,cursor)+fontspacing
    leftspace=(ledsize[0]-cursor+alignment)/2
    if cursor>ledsize[0]:
        error("Unable to create image: Name ("+name+") too long!")
    if b_addAnd:
        cursor-=relativeAndPosition
        andsymbol=Image.open(andpath,"r")
        addAnd(image,andsymbol,cursor)
    tosave=newLED()
    tosave.paste(image,(leftspace,0))
    return tosave

def saveImage(image,filename=imagefilename,path=outputfolder):
    image.save(path+filename+imagetyp)

def generateAndSave(name,b_addAnd=True):
    if name=="":
        error("Unable to create image: Name is empty!")
    else:
        name=unicode(name)
        #name=name.upper()
    img=generateImage(name,b_addAnd)
    saveImage(img)
    return "done"
    
def getStartOptions():
    parameter=sys.argv
    if len(parameter)==1:
        return 1
    elif len(parameter)==3:
        if parameter[1]=="-n":
            return 2
        elif parameter[1]=="-l":
            return 3
        else:
            return 0
    elif len(parameter)==4:
        if parameter[1]=="-n" and parameter[3]=="-nofriend":
            return 4
        elif parameter[1]=="-l" and parameter[3]=="-nofriend":
            return 5
        else:
            return 0
    else:
        return 0

def startConsole():
    name=raw_input("Please enter Text or Name:\n")
    nfriends=raw_input("Add & FRIENDS? (yes(d)/no):\n")
    sure=raw_input("Are you sure to generate: "+name+" & Friends? (yes/no(d)):\n")
    if sure in ["yes","y"]:
        generateAndSave(name.decode("utf-8"),not nfriends in ["no","n"])

def main():
    mode=getStartOptions()
    if mode==0:
        error("Unable to create image: Wrong parameter!")
    elif mode==1:
        startConsole()
    elif mode==2:
        generateAndSave(sys.argv[2].decode("utf-8"))
    elif mode==3:
        try:
            f=open(sys.argv[2])
        except:
            error("Unable to create image: Listfile not found!")
        try:
            names=f.read().decode("utf8")
        except:
            error("Unable to create image: Listfile not UTF-8 encoded!")
        names=names.replace("\r","").split("\n")
        for name in names:
            if name != "":
                generateAndSave(name)
    elif mode==4:
        generateAndSave(sys.argv[2].decode("utf-8"),False)
    elif mode==5:
        try:
            f=open(sys.argv[2])
        except:
            error("Unable to create image: Listfile not found!")
        try:
            names=f.read().decode("utf8")
        except:
            error("Unable to create image: Listfile not UTF-8 encoded!")
        names=names.replace("\r","").split("\n")
        for name in names:
            if name != "":
                generateAndSave(name,False)

if __name__ == "__main__":
    main()