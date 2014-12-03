#!/usr/bin/python
import subprocess as sub
from config import *
import pty,os,sys,smtplib

def error():
    smtpserver = smtplib.SMTP(gmail_server,gmail_server_port)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: LED-Anzeige <' + gmail_user + '>\n' + 'Subject: ERROR: SCL-Uploader: TIME OUT! \n'
    msg  = header 
    msg +='\nDer SCL-Uploader lieferte 5 Mal in Folge den Fehler:\nUpload failed: Operation timed out\nBitte die naechsten Schritte einleiten!\n'
    smtpserver.sendmail(gmail_user, to, msg)
    smtpserver.close()

def sendsuccess():
    smtpserver = smtplib.SMTP(gmail_server,gmail_server_port)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: LED-Anzeige <' + gmail_user + '>\n' + 'Subject: Erfolg: SCL-Uploader neu! \n'
    msg  = header 
    msg +='\nDer SCL-Uploader hat das Bild erfolgreich hochgeladen!\n'
    smtpserver.sendmail(gmail_user, to, msg)
    smtpserver.close()

master, slave = pty.openpty()

scl=sub.Popen([workingfolder+"scl-uploader","-w",outputfolder,ledip],stdout=slave,stderr=slave,close_fds=True)
stdout = os.fdopen(master)
counter=0
while True:
	try:
		output = stdout.readline()
	except:
		scl.terminate()
		sys.exit(0)
	if "Upload failed: Operation timed out" in output and counter < 4:
		counter+=1
		os.popen("touch "+outputfolder+"PLAYLIST.LY")
	if "Upload successful" in output:
		counter=0
		#sendsuccess()
	if counter>4:
		error()
		counter=0
	if counter == 4:
		counter+=1