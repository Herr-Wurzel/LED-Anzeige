#!/usr/bin/python
'''
Created on 13.07.2012

@author: Christian Pollmann

'''

ledip="172.31.16.25"
# sommerzeiten=["+01:00","+02:00"]
# sommerzeit=sommerzeiten[1]
# Die Sommerzeit-Problematik wurde am 3.4.13 anders geloest (Variable summtime in fillcalender.py und syncLED.py).
# Sollte die alte Mimik wiederhergestellt werden, muss u.a. die Variable wieder in fillcalender.py und syncLED.py importiert werden
defaultname="SCHOLZ"
friendsword="FRIENDS"

feiertage=["01.01.2013","29.03.2013","01.04.2013","01.05.2013","09.05.2013","20.05.2013","03.10.2013","24.12.2013","25.12.2013","26.12.2013","31.12.2013","01.01.2014","18.04.2014","21.04.2014","01.05.2014","29.05.2014","09.06.2014","03.10.2014","24.12.2014","25.12.2014","26.12.2014","31.12.2014"]

# FOLDER
workingfolder="/Users/Shared/sf-led_anzeige/"
outputfolder="/Users/Shared/output/"
fontfolder="/Library/Fonts/Legacy-OpenType/"

# FILES
fontfile=fontfolder+"LegacySansS&F-LogoType.otf"
lastnametxt=workingfolder+"lastname.txt"
weektxt=workingfolder+"woche.txt"
andpath=workingfolder+"and.png"
heartpath=workingfolder+"herz.png"
fullpngpath=workingfolder+"full.png"
heartwidth=29
imagefilename="CURRENT"
imagetyp=".PNG"

# SIZES
ledsize=(1168,40)
fontsize=86
fontspacing=12
fontheight=-7
middlespace=98
alignment=12
relativeAndPosition=354

# IMAGE SETTINGS
imagemode="1"
backgroundcolor=1
fontcolor=0

# GOOGLE
gmail_user = 'cal.sfb.it@gmail.com'
gmail_pwd = 'python666script'
gmail_server = 'smtp.gmail.com'
gmail_server_port = 587
to = 'norbert.wurzel@s-f.com'

# PLAYLISTS

dauerplaylist='''[Program1]
Timer1=009901120131010700002359
Timer2=000000000000000000000000
Timer3=000000000000000000000000
Timer4=000000000000000000000000
Timer5=000000000000000000000000
Timer6=000000000000000000000000
Timer7=000000000000000000000000
Timer8=000000000000000000000000
MainScreen=1
Screen=1
[Program1_Screen1]
Position=2928,0,1168,40
ItemCount=1
Item1=P,CURRENT.PNG,1,8,3600'''

wechselplaylist='''[Program1]
Timer1=009901120131010700002359
Timer2=000000000000000000000000
Timer3=000000000000000000000000
Timer4=000000000000000000000000
Timer5=000000000000000000000000
Timer6=000000000000000000000000
Timer7=000000000000000000000000
Timer8=000000000000000000000000
MainScreen=1
Screen=1
[Program1_Screen1]
Position=2928,0,1168,40
ItemCount=2
Item1=P,CURRENT.PNG,1,8,30
Item2=P,SCHOLZ.PNG,1,8,30'''
