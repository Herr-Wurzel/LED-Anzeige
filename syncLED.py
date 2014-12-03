#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 17.07.2012

@author: Christian Pollmann and Norbert Wurzel
'''

#Portierung zur Google API v3 von Norbert Wurzel (2014)

#Notwendige Importierungen
import pty,os,sys,smtplib
from config import gmail_user,gmail_pwd,lastnametxt,defaultname,outputfolder,wechselplaylist,dauerplaylist,weektxt
from generateImages import generateAndSave,generateImage
import gdata.calendar.service
from gcalAuth import *
from time import *
from config import *
import time

global event

import gcalAuth

#Auslesen des letzten verwendeten Namens aus der Datei lastname.txt
def getLastname(lastnametxt=lastnametxt):
    try:
        f=open(lastnametxt,"r")
    except:
        f=open(lastnametxt,"w")
        f.close()
        f=open(lastnametxt,"r")
    lastname=f.read()
    f.close()
    return lastname

def cpPlaylist(wechsel=False):
    f=open(outputfolder+"PLAYLIST.LY","w")
    if wechsel:
        f.write(wechselplaylist)
    else:
        f.write(dauerplaylist)
    f.close()
    return "done"

def triggerUpload():
    #not supported in this version!
    pass

#Ist der Event-Titel anders als vor 30 Sekunden? -> dann schreibe aktuellen Titel in lastname.txt und initiiere den Upload
def makeChange(event_titel,addFriend=False,wechsel=False,lastnametxt=lastnametxt):
    lastname=getLastname()
    ##print "--------------"
    ##print "*** Zeit:",curTime
    ##print "*** Lastname: ",lastname
    ##print "*** Vergleich mit ", event_titel+str(addFriend)+str(wechsel)
    if lastname.decode('utf-8')!=event_titel+str(addFriend)+str(wechsel):
        #sendsuccess()
        ##print "*** MAKECHANGE mit ",event_titel
        ##print "--------------"
        f=open(lastnametxt,"w")
        f.write(event_titel.encode('utf-8')+str(addFriend)+str(wechsel))
        f.close()
        if generateAndSave(event_titel,addFriend) == "done":
            if cpPlaylist(wechsel)=="done":
                triggerUpload()

def sendsuccess():
    smtpserver = smtplib.SMTP(gmail_server,gmail_server_port)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: LED-Anzeige <' + gmail_user + '>\n' + 'Subject: MakeChange laeuft \n'
    msg  = header 
    msg +='\nDer SCL-Uploader hat das Bild erfolgreich hochgeladen!\n'
    smtpserver.sendmail(gmail_user, to, msg)
    smtpserver.close()


#lege Zeitraum von gestern 0 Uhr bis heute Mitternacht fest
def genStartEnd():
    global start_date
    global end_date
    start_date=time.strftime('%Y-%m-%dT00:00:00.000+01:00',time.localtime(time.time()+60*60*1))
    end_date=time.strftime('%Y-%m-%dT23:59:59.000+01:00',time.localtime(time.time()+60*60*25))
    return (start_date,end_date)

#Ermittle alle relevanten Infos für das fragliche Event (Titel, Start- und Endezeit, Ort, ID)
def getEventinfos(event):
    global event_titel
    global event_ID
    global addFriend
    global event_anfang
    global event_ende
    global event_where
    event_anfang="*leer"
    event_ende="*leer"
    addFriend=False
    event_where="*leer"
    event_titel = event.get(u'summary')
    if event_titel[-10:len(event_titel)]==" & FRIENDS":
     event_titel=event_titel[0:-10]
     addFriend = True
    else:
     addFriend = False
    event_ID =  event.get(u'id')
    event_where = event.get(u'location')
    event_a = event.get(u'start')
    if event_a:
     event_anfang = event_a[u'dateTime']
    event_e = event.get(u'end')
    if event_e:
     event_ende = event_e[u'dateTime']
#    ###print  "C ",event_titel," ",addFriend," ",event_anfang," ",event_ende," ",event_where," ",event_ID
    return (event_titel,addFriend,event_anfang,event_ende,event_where,event_ID)

#Ermittle die aktuelle Zeit im Google-kompatiblen Format
def currentTime():
 lt = localtime()
 curTime = mktime(lt)
 curTime = strftime("%Y-%m-%dT%H:%M:%S+01:00",lt)
 return curTime

#Pruefe, ob das fragliche Event gerade jetzt laeuft -> falls ja, pruefe, ob es ein neues Event ist
def checkEvent(an_event):
    global curTime
    event_titel,addFriend,event_anfang,event_ende,event_where,event_ID=getEventinfos(an_event)
    curTime = currentTime()
    if ((curTime>event_anfang) and (curTime<event_ende)):
        ##print "Start:   ",event_anfang
        ##print "Current: ",curTime
        ##print "Ende:    ",event_ende
        makeChange(event_titel,addFriend,event_where=="automatic" or event_where=="wechsel")
        return True
    else:
#Nachts um 2 Uhr wird immer Scholz & Frinds erstellt
        if time.strftime("%H-%M")=="02-00":
         generateImage(event_titel,addFriend)
         return False
    
# wochentagsabhaengige Aenderung der Verschiebung, um Abnutzung der LEDs zu verhindern
def chgdefname():
    lt=localtime()
    weekday=strftime("%w", lt)
    f=open(weektxt,"w")
    defname=defaultname
    if weekday=="2":
        defname=" "+defaultname
    if weekday=="4":
        defname=" "+defaultname
    if weekday=="6":
        defname=" "+defaultname
    f.write(defname)
    f.close()
    return defname


def start():
    #sendsuccess()
    gotevent=False
    chgdefname()
    page_token= None
    genStartEnd()
    events = service.events().list(calendarId=calID, pageToken=page_token, timeMin=start_date, timeMax=end_date).execute()
    for event in events['items']:
     event_titel,addFriend,event_anfang,event_ende,event_where,event_ID = getEventinfos(event)
     gotevent=gotevent or checkEvent(event)
     checkEvent(event)
     if not gotevent:
        makeChange(chgdefname(),True)

def main(loop=False):
    if loop:
#        try:
            while True:
                start()
                time.sleep(30)
#        except:
            import sys
            sys.stdout.write("\r")
    else:
        start()

main(True)