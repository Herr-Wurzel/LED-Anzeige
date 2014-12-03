#!/usr/bin/python
# -*- coding: utf-8 -*-

import pty,os,sys,smtplib

import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

from config import *

# GOOGLE
gmail_user = 'cal.sfb.it@gmail.com'
gmail_pwd = 'python666script'
gmail_server = 'smtp.gmail.com'
gmail_server_port = 587
to = 'norbert.wurzel@s-f.com'


def senderror():
  if send_marker == "0":
    smtpserver = smtplib.SMTP(gmail_server,gmail_server_port)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: LED-Anzeige <' + gmail_user + '>\n' + 'Subject: Autorisierungsfehler im LED-Kalenderscript! \n'
    msg  = header 
    msg +='\nDie Autorisierungsmimik im KalenderScript hat einen Fehler gemeldet.\n\n1.) Entferne auf dem Konsolenrechner die Datei /Users/Shared/sf-led_anzeige/calendar.dat\n\n2.) Fuehre im Terminal /Users/Shared/sf-led_anzeige/gcalAuth.py aus (als root)\n\n3.) Folge den Anweisungen.\n\n\nBei Google anmelden mit\n\ngmail_user = cal.sfb.it@gmail.com\n\ngmail_pwd = python666script\n\n\nDas Script erstellt jetzt eine neue calendar.dat erstellt, in der die Autorisierungscredentials hinterlegt sind. \n\n\nnorb-)\n'
    smtpserver.sendmail(gmail_user, to, msg)
    smtpserver.close()

calID = '02sho42ncasrc3uqklfjmautgg@group.calendar.google.com'

FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret are copied from the API Access tab on
# the Google APIs Console
FLOW = OAuth2WebServerFlow(
    client_id='420050955256-u66gpgninsjebhqp4dkkv4bqvdf28nl3.apps.googleusercontent.com',
    client_secret='Rp2F45kQxwTJFzT3g3i9wTci',
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='Python/2.7')

# To disable the local server feature, uncomment the following line:
FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
storage = Storage(workingfolder+'calendar.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
 credentials = run(FLOW, storage)
 exit(0)
 
# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API. Visit
# the Google APIs Console
# to get a developerKey for your own application.
service = build(serviceName='calendar', version='v3', http=http,
       developerKey='AIzaSyDwqIHUdJsohgc0ZGQPifc2CWQI5xZ27s0')
       
