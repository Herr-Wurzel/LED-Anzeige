#!/usr/bin/python
# -*- coding: utf-8 -*-

#Portierung ´zur Google API v3 von Norbert Wurzel (2014)


import gflags
import httplib2

import time,atom,sys
from gcalAuth import * 
from config import *

global lastAutomatic
global event

#Beginn und Ende der fraglichen 7-Tage-Frist ermitteln     
def genStartEndWeek(week):
 global start_date
 global end_date
 start_date = start_date=time.strftime('%Y-%m-%d',time.localtime(time.time()+60*60*24*7*(week)+3600))
 end_date = end_date=time.strftime('%Y-%m-%d',time.localtime(time.time()+60*60*24*7*(1+week)+3600))
 start_date = start_date+'T00:00:00+05:30'
 end_date = end_date+'T00:00:00+05:30'

#Event-Infos ermitteln (Titel, Start, Ende, Ort, ID)
def getEventinfos(event,alle=True):
    global event_titel
    global event_ID
    event_anfang="*leer"
    event_ende="*leer"
    event_titel = event.get(u'summary')
    event_ID =  event.get(u'id')
    event_where = event.get(u'location')
    event_a = event.get(u'start')
    if event_a:
     event_anfang = event_a[u'dateTime']
    event_e = event.get(u'end')
    if event_e:
     event_ende = event_e[u'dateTime']
    if alle:
      return (event_titel,event_where,event_anfang,event_ende,event_ID)
    else:
     return event_where

#letztes automatisch erstelltes Event ermitteln
def getlastAutomatic():
 global event
 global lastAutomatic
 global page_token
 lastAutomatic = ""
 lastTime=0
 page_token = None
 genStartEndWeek(-1)
 while True:
  events = service.events().list(calendarId=calID, pageToken=page_token, timeMin=start_date).execute()
  for event in events['items']:
   event_titel,event_where,event_start,event_ende,event_ID = getEventinfos(event)
   if event_where=="automatic":
    if event_ende>lastTime:
     lastAutomatic=event_titel
     lastTime=event_ende
  page_token = events.get('nextPageToken')
  if not page_token:
    break
 return lastAutomatic

def deleteEvent(event_ID):
 service.events().delete(calendarId=calID, eventId=event_ID).execute()

#die zuletzt automatisch erstellen Eintraege loeschen, um Dopplungen zu verhindern
def deleteNewAutomatic(autoexit=False):
 page_token = None
 genStartEndWeek(0)
 events = service.events().list(calendarId=calID, pageToken=page_token, timeMin=start_date, timeMax=end_date).execute()
 for an_event in events['items']:
  event_titel,event_where,event_start,event_ende,event_ID = getEventinfos(an_event)
  if event_where=="automatic":
   deleteEvent(event_ID)
  if autoexit:
   sys.exit()

def genBlock(blockanfang,blockende,freizeit):
    block=list()
    for i in range(blockanfang,blockende):
        if i in freizeit:
            if block==[]:
                block.append([i,i+1])
            else:
                if block[len(block)-1][1]==i:
                    block[len(block)-1][1]=i+1
                else:
                    block.append([i,i+1])
    return block

def genDayBlock(day,events):
    if time.strftime("%a",time.localtime(time.time()+day*60*60*24+3600))[0]=="S":
        return list()
    if time.strftime("%d.%m.%Y",time.localtime(time.time()+day*60*60*24+3600)) in feiertage:
        return list()
    anfang=time.strftime("%Y-%m-%d-09-00-00",time.localtime(time.time()+day*60*60*24+3600))
    anfang=int(time.mktime(time.strptime(anfang, "%Y-%m-%d-%H-%M-%S")))
    freizeit=[[],[],[]]
    for h in range(0,len(freizeit)):
        for zeit in range(anfang+3*60*60*h,anfang+3*60*60*(h+1)):
            istfrei=True
            for event in events:
                if zeit>=event[0] and zeit<=event[1]:
                    istfrei=False
            if istfrei:
                freizeit[h].append(zeit)
    blockzeit=time.strftime("%Y-%m-%d-09-00-00",time.localtime(time.time()+day*60*60*24+3600))
    blockzeit=int(time.mktime(time.strptime(blockzeit, "%Y-%m-%d-%H-%M-%S")))
    block=list()
    block.append(genBlock(blockzeit,blockzeit+3*60*60,freizeit[0]))
    block.append(genBlock(blockzeit+3*60*60,blockzeit+6*60*60,freizeit[1]))
    block.append(genBlock(blockzeit+6*60*60,blockzeit+9*60*60,freizeit[2]))
    return block

def getNextName(prevName):
    allNames=getNames()
    counter=0
    while allNames[counter % len(allNames)]<=prevName and counter<len(allNames):
        counter+=1
    return allNames[counter % len(allNames)]

def getNames():
    f=open(workingfolder+"namelist.txt")
    names = f.read().replace("ß","SS").decode("utf-8").replace("\r","").upper().split("\n")
    f.close()
    #remove duplicates
    names=list(set(names))
    names.sort()
    while names[0]=='':
        names.pop(0)
    for i in range(0,len(names)):
        names[i]+=" & FRIENDS"
    return names

def createNewAutoEvents(lastname):
 events = service.events().list(calendarId=calID, pageToken=page_token, timeMin=start_date).execute()
 block=[]
 for day in range(0,7):
  block+=genDayBlock(day,events)
  while True:
   try:
    block.pop(block.index(list()))
   except:
    break
 for entrytimes in block:
  lastname=getNextName(lastname)
  for entrytime in entrytimes:
   createEntry(lastname,entrytime)

def createEntry(name,entrytime):
 timezone = "Europe/Berlin"
 start=time.strftime("%Y-%m-%dT%H:%M:%S.000",time.localtime(entrytime[0]))
 end=time.strftime("%Y-%m-%dT%H:%M:%S.000",time.localtime(entrytime[1]))
 start=start+"+01:00"
 end=end+"+01:00"

 event = {
  'summary': name,
  'location': 'automatic',
  'start':  {
    'dateTime': start
  },
  'end': {
    'dateTime': end
  },
  'description': '''ACHTUNG: Der Name des Termins ist Case sensitive!

Das WO-Feld gibt an, ob ein Eintrag automatisch erstellt wurde bzw. ob sich ein Bild mit dem Scholz-Bild abwechseln soll.

"automatic" ist ein Eintrag, der automatisch erstellt wurde und somit auch ggf. automatisch geloescht wird! Alle "automatic" Eintraege wechseln sich in 30 Sekunden Abstaenden mit dem Scholz-Bild ab.

"wechsel" kann man bei einem manuellen Eintrag eintragen, dass sich das Bild mit dem "Scholz & Friends" Bild in 30 Sekunden Abstaenden abwechselt. Diese Eintraege werden NICHT automatisch geloescht!

"" ist ein manueller Eintrag, welcher nicht automatisch geloescht wird und dauerhaft - somit ohne 30 Sekunden Wechsel - dargestellt wird. Diese Eintraege werden NICHT automatisch geloescht!'''
 }

 created_event = service.events().insert(calendarId=calID, body=event).execute()


global lastname
deleteNewAutomatic()
lastname = getlastAutomatic()

createNewAutoEvents(lastname)

