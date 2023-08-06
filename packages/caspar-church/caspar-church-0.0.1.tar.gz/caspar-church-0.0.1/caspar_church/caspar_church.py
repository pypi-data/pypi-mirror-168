print('CasparCG Church 1.21')
#Copyright (C) <2020>  <Jeffrey Rydell>

#############################################################################################################
#    
# ###################  CHANGELOG #################
#   from version 1.2.0
#       Now works with CasparCG 2.3    
#       When used with "CasparCG version 2.3 ", in update media listbox, fixed compatibility error in the parsing of media details.
#       Fixed the PrintFrame function.
#       Fixed bug prevented saving changes to a "Bible verse" slide.
#       Added the Alt + b hotkey for loading the Bible form.
#       fixed bug, when testing a slide with a movie attached sometimes only the first frame will play.
#       Added button to refresh Rundown.
#
#       known issues
#           when editing a media file looping doesn't always load.
#       
#       
#   from v 1.1.9 
#       In the "select media" dialog, when a media fie is previewed the command line will now print the current frame. pressing pause(f8) will return the paused frame_number(well a number close to that frame).
#       removed the master media ist form.(didn't really serve a purpose at the moment).
#       f10 now sends CG NEXT command(for use in controlling animated templates)
#       Cleaned up the displaying of media titles in the rundown.
#       Various code cleanups
#       Fixed bug in the load_song function that prevented a song from loading if sudio was attached.
#       Fixed bug after deleting rundown items or slides the rundown wouldn't refresh properly.
#       Fixed bug in "select Media" the "Seek" and "Legnth" fields reset upon selecting another video file.
#       Fixed bug in "server settings" the Bible profile wouldn't automatically be added. 
#       Fixed 2 bugs in saving Bible verses to current document.
#       Eliminated redundant code for creating scrolling and sortable frames.

#
#   Known bugs
#       You using the handles you cannot "drag" to trim a video file all the way to the final frame. this can be overcome by manually entering the video legnth.( depending on usage may not be an issue.)
#
#   from v1.1.8  
#       Fixed a bug that prevented saving changes to a song. 
#       Fixed the verseedit form so that songs could be edited.
#       Fixed a bug that when saving a rundown the rundown would disappear entirely.
#       Fixed the rundown loading function.
#       Fixed bud that prevented Audio files form playing.
#       Fixed a bug in the "self.Update_thumbnail_index()" that would occasionaly prevent loading.
#       In the "select media" dialog, replaced the "file selection listbox" with a list of buttons with thumbnails. 
#       
#       ###NOT AVAILABLE YET###
#      
#
#   when deleteing rundown items and slides the list doesn't reshuffle to fill in the missing gap.
#   In "edit song" verses are not displayed in order of verse id?
#   Features to add                                                                                             
#       For version 1.2
#           Fix Bible lookup     pip3 install Bible3     pip install python-scriptures
#           Add Messages
#           slides can be sorted
#           Verse splitter tool
#           Add ccli
#           add propresenter 6, openlp and powerpoint support?  pip3 install striprtf
#           add openlyrics support


#  ###### AMCP Plugin bugs  ######
#   Pause command in amcp plugin is actually play
#   cannot add stream consumer bug plugin insists on using quotes 


# ######  Wishlist  #######

    # Messaging Functions 
    # Guest Speaker Index
    # Add preview images for templates
    # Add overlays
    # add autoplay for slides (slide show),  Doesent Loop
    # up down arrow keys control next media
    # pageUp pageDown control next document 
    # in newverse add reset all media
    # call command passes parameters to currently playing file
    # shift delete rundown items in groups.
    

    # jankey
    # ProgramBug            
#############################################################################################################


from typing import Any
from amcp_pylib.core import Client#, ClientAsync
from amcp_pylib.module.query import VERSION, BYE, TLS, CLS, INFO, INFO_CHANNELS,INFO_QUEUES, CINF, INFO_SYSTEM ,INFO_SERVER, HELP_CONSUMER,HELP,HELP_PRODUCER
from amcp_pylib.module.mixer import MIXER_CLEAR,CHANNEL_GRID
from amcp_pylib.module.template import CG_ADD, CG_PLAY, CG_STOP, CG_UPDATE, CG_INFO, CG_CLEAR, CG_UPDATE, CG_NEXT
from amcp_pylib.module.data import DATA_LIST, DATA_REMOVE, DATA_RETRIEVE, DATA_STORE
from amcp_pylib.module.basic import LOADBG, LOAD, PLAY, STOP, CLEAR, PAUSE, RESUME,ADD,CALL
from amcp_pylib.module.thumbnail import THUMBNAIL_RETRIEVE,THUMBNAIL_LIST, THUMBNAIL_GENERATE_ALL,THUMBNAIL_GENERATE


from time import sleep
import time

import tkinter as tk
from tkinter import filedialog as fd

from tkinter import ttk
from tkinter import *
from tkinter import colorchooser 

from Widget_frames import *
from CC_Utility import *
# Widget_frames.APPapplication = APPapplication


import math
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
import textwrap
import threading
import sys
import os
import datetime

import scriptures
# import asyncio
# from amcp_pylib.core import ClientAsync

#client_async = ClientAsync()
#asyncio.new_event_loop().run_until_complete(client_async.connect("127.0.0.1", 6969))


############################# start of misc functions
# def sortBook(event): # in the Bible form book listbox this function will show only the books that match the key entered.
#     APPapplication.ref_book_entry.delete(0, END)     
#     for x in range(1 ,len(BibleXML)):
#         BookName = BibleXML[x].get('bname')
#         if IsNumber(event.keysym) == False:
#             if IsNumber(BookName[:1]):
#                 BookName = BookName[:3]
#                 BookName = BookName[2:].lower()
#             else:
#                 BookName = BookName[:1].lower()
#         else:
#             BookName = BookName[:1].lower()
#         if BookName == event.keysym:
#             APPapplication.ref_book_entry.insert(END, BibleXML[x].get('bname'))

####################### start of media trim functions   ##############################

def Media_range_motion(event):
    Widget = event.widget
    Master = Widget.Container_index# gets the widget frame array of the widget's parent frame 
    App = Widget.Application
    Source_index = Widget.index 
    widget_info = Widget.place_info()
    Frames = Widget.Frames
    Frames_divisor = Frames / 380
    framerate = Widget.framerate

    widget_x = int(widget_info.get('x'))

    try:
        old_seek = int(App.Media_Seek_entry.get())
    except:
        old_seek = 0
    NEW_x =  widget_x  + event.x

    # start widget placement code
    if Source_index == 1:
        widget_0_info = Master[0].place_info()
        start_index = int(widget_0_info.get('x'))
    else:
        start_index = 0
    
    if Source_index == 0:
        widget_1_info = Master[1].place_info()
        end_index = int(widget_1_info.get('x'))
    else:
        end_index = 380

    if NEW_x >= end_index:
        NEW_x = end_index

    if NEW_x <= start_index:
        NEW_x = start_index

    Widget.place(x=NEW_x)
    # end widget placement code
    if Source_index == 0:
        Seek = str(round(Frames_divisor * NEW_x))
        Legnth = str(round(Frames_divisor * end_index) - old_seek)

        start = round(int(Seek) / framerate)
        start_time = str(datetime.timedelta(seconds=start))
        App.trim_media_Start_time_label.configure(text=start_time)
        end_time = round(int(Legnth) / framerate)
    else:
        
        Legnth = str(round(Frames_divisor * NEW_x) - old_seek)

        end = int(Legnth) + old_seek
        end_t = round(end / framerate)
        end_time = str(datetime.timedelta(seconds=end_t))
        App.trim_media_End_time_label.configure(text=end_time)

    if Source_index == 0:  
        App.Media_Seek_entry.delete(0, END)
        App.Media_Seek_entry.insert(END, Seek)

    App.Media_Legnth_entry.delete(0, END)
    App.Media_Legnth_entry.insert(END, Legnth)

def Media_range_end(event):
    Widget = event.widget
    App = Widget.Application
    Source_index = Widget.index
    if Source_index == 0:
        App.Preview_selected_media("Start", 80)
    if Source_index == 1:
        App.Preview_selected_media("End", 80)

def Media_trim(event):
    # retreves seek and legnth, removes hotkey characters if any are found.
    App = APPapplication
    Seek = App.Media_Seek_entry.get()
    try:
        Seek = int(Seek)
    except:
        Seek = int(Seek[:-1])
        App.Media_Seek_entry.delete(0, END) 
        App.Media_Seek_entry.insert(END, str(Seek))
    Legnth = App.Media_Legnth_entry.get()
    
    try:
        Legnth = int(Legnth)
    except:
        Legnth = int(Legnth[:-1])
        App.Media_Legnth_entry.delete(0, END)
        App.Media_Legnth_entry.insert(END,str(Legnth))

    loadframes = False

    if event.keysym == 'q' or event.keysym == 'e':
        Widget = App.trim_media_Start_slider
        loadframes = True

    if event.keysym == 'a' or event.keysym == 'd':
        Widget = App.trim_media_End_slider
        loadframes = True

    if loadframes == True:
        Frames = Widget.Frames
        framerate = Widget.framerate
        Frames_divisor = Frames / 380

    if event.keysym == "w":
        App.Preview_selected_media("Start", 100)
    if event.keysym == "s":
        App.Preview_selected_media("End", 100)

    if event.keysym == "q":
        Seek -= 1
        Legnth += 1

    if event.keysym == "e":
        Seek += 1
        Legnth -= 1

    if event.keysym == "a":
        Legnth -= 1

    if event.keysym == "d":
        Legnth += 1
    
    if Seek >= Frames:
        Seek = Frames
    if Legnth >= Frames:
        Legnth = Frames

    if Seek >= Seek + Legnth:
        Seek = Seek + Legnth

    if Seek <= 0:
        Seek = 0
    if Legnth <= 0:
        Legnth = 0

    if event.keysym == 'q' or event.keysym == 'e':
        App.Media_Seek_entry.delete(0, END)
        App.Media_Legnth_entry.delete(0, END)

        App.Media_Seek_entry.insert(END, str(Seek))
        App.Media_Legnth_entry.insert(END, str(Legnth))
        start = round(Seek / framerate)
        start_time = str(datetime.timedelta(seconds=start))
        App.trim_media_Start_time_label.configure(text=start_time)
        NEW_x = Seek / Frames_divisor
        Widget.place(x=NEW_x)

    if event.keysym == 'a' or event.keysym == 'd':
        APPapplication.Media_Legnth_entry.delete(0, END)
        App.Media_Legnth_entry.insert(END, str(Legnth))

        end = Legnth + Seek
        end_t = round(end / framerate)
        end_time = str(datetime.timedelta(seconds=end_t))
        App.trim_media_End_time_label.configure(text=end_time)
        NEW_x = (Seek + Legnth) / Frames_divisor
        Widget.place(x=NEW_x)

#######################################  end of media trim functions

# def test_test(event):
#     if event.keysym == "i":
    
#     if event.keysym =="k":

#     if event.keysym =="j":

#     if event.keysym =="l":

# def Rezize_frames(event):
#     # global Last_Height
#     # global Last_Width
#     global resize_timer
#     print(event)
#     try:
#         y = APPapplication.Last_Height
#     except:
#         APPapplication.Last_Height = event.height
#         APPapplication.Last_Width = event.width
#         APPapplication.resize_Frame = False
    
#         # resize_timer = round(time.time())
#     # print(resize_timer)
#     # if time.time() >= resize_timer + 2:
#         # resize_timer = round(time.time())  

#     if event.height != APPapplication.Last_Height:
#         # APPapplication.
#         # print("event.height: ", event.height,"event.width: " , event.width)
#         # print("APPapplication.Last_Height: ", APPapplication.Last_Height, "\tAPPapplication.Last_Width: ", APPapplication.Last_Width)
#         APPapplication.Last_Width = event.width
#         APPapplication.Last_Height = event.height
#         APPapplication.Slide_document_canvas.configure(height=event.height -140)
#         APPapplication.resize_Frame = True
#     # if event.width != APPapplication.Last_Width:

# #         Last_Height = event.height
# #         Last_Width = event.width
#     # #         # print(event)
#     # #         # print(event.height)
#     # #         APPapplication.Slide_document_canvas.configure(height=event.height -100)

# def Resize_framesB(event):
#     global old_width
#     global old_height
#     Height = APPapplication.winfo_height()
#     Width = APPapplication.winfo_width()
    
#     try:
#         y = old_height
#     except:
#         old_height = Height
#         old_width = Width
#         # APPapplication.resize_Frame = False
#     if APPapplication.resize_Frame == True:
#         if Height != old_height:
#             APPapplication.Slide_document_canvas.configure(height=Height -400)
#             old_height = Height
#             APPapplication.resize_Frame = False
#             APPapplication.Slide_document_canvas.configure(scrollregion=APPapplication.Slide_document_canvas.bbox("all"))
#         if Width != old_width:
#             APPapplication.Slide_document_canvas.configure(width=Width -700)
#             old_width = Width
#             APPapplication.resize_Frame = False
#             APPapplication.Slide_document_canvas.configure(scrollregion=APPapplication.Slide_document_canvas.bbox("all"))


    # print("test1111:",APPapplication.winfo_height())
    # print(APPapplication.resize_Frame)

    # try:
        # if APPapplication.resize_Frame == False:
        # Height = APPapplication.winfo_height()
        # Width = APPapplication.winfo_width()
            # print('APPapplication.New_Height: ' + str(APPapplication.New_Height))
            # print('APPapplication.New_Width: ', str(APPapplication.New_Width))
        #     APPapplication.resize_Frame = False
        #     newHeight = APPapplication.New_Height
        #     newWidth = APPapplication.New_Width

        # APPapplication.Slide_document_canvas.configure(height=Height -400 , width=Width -700)
        # APPapplication.Slide_document_canvas.configure()
        
    # except:
        # y=None


################################## start of caspar functions

# def stream_channel(channel,consumer_index): # mostly test code, will not work plugin buggy
#     # stream = "STREAM"
#     # test = client.send(PLAY(video_channel=channel, layer=10, html='HTML', clip='http://www.google.com'))
#     # test = client.send(STREAM(video_channel=channel))# parameters='udp://<client_ip_address>:9251'
#     # test = client.send(ADD(video_channel=channel,consumer='STREAM',parameters=""))
#     # TEST = client.send(CALL(video_channel=channel,param='udp://<client_ip_address>:9251 -format mpegts -vcodec libx264 -crf 25 -tune zerolatency -preset ultrafast -vf scale=288:162'))
#     # client.send(ADD(video_channel=channel, consumer="IMAGE", parameters="TESTIMAGE"))
#     # ADD 1 IMAGE filename
#     # print(test.data_str)
#     client.send(PLAY(video_channel=1, layer=10, clip="dshow://video=USB Video Device"))#
#     # PLAY 1-1 “dshow://video=Integrated Webcam”

def load__passage(event):
    APPapplication.get_passage()
def launch_bible(event):
    try:
        APPapplication.loadverse_frm.destroy()
    except:
        APPapplication.load_bible()


def Print_frame(seek, legnth, media_details):
    global PauseState
    framerate = fraction_to_float(media_details[4]) 
    # seconds = round(media_seconds(filename,0,media_details))
    # duration = str(datetime.timedelta(seconds=seconds))
    # frame = seek
    # print("test111")
    # legnth = int(seek) 
    # print(legnth)
    # legnth = int(legnth)
    legnth = int(media_details[3])
    thread1 = threading.Thread(target=print_frameb, args=(seek, framerate, legnth))
    thread1.start()
    # while pausestate = False:
        # self.select_media_frm.title("Select Media Frame=: " + str(frame))
        # self.after(1000, reset_New_media_playing)

    
def print_frameb(seek, framerate, legnth):      
    global PauseState
    frame = int(seek)
    # print("test222")
    framerate = 1 / framerate
    print("framerate: " + str(framerate))
    print("legnth: " + str(legnth))
    print("frame: " + str(frame))
    while frame <= legnth:
        frame += 1
        print("frame: " + str(frame))
        time.sleep(framerate)
        if PauseState:
            break
            time.sleep(2)
            PauseState = False


def save_channel_template_index(event):# buggy function?
    global channel_templates_active_index
    try:
        channel_templates_active_index = APPapplication.channel_templates_listbox.index(ACTIVE)
        print("channel_templates_active_index: " + str(channel_templates_active_index))
    except:
        y=None


def load_thumbnail_xml():
    global ThumbnailXML
    xmlfile = replace_char(os.getcwd(),'\\','/') + "/Thumbnail.xml"
    parser3 = ET.XMLParser()
    try:
        Thumbnail = ET.parse(xmlfile,parser3)

        ThumbnailXML = Thumbnail.getroot()
        return True
    except:
        ThumbnailXML = ET.Element('Thumbnails')
        return False



def media_seconds(filename, legnth, mediadetails):
    # mediadetails = get_media_details(filename)
    try:
        if mediadetails[1] == "MOVIE":
            if legnth != 0:
                frames = legnth
            else:
                frames = int(mediadetails[3])
            framerate = fraction_to_float(mediadetails[4])
            seconds = frames / framerate
            return seconds
        else:
            return 0
    except:
        return 0

def get_media_details(filename):
    try:
        Mediainfo = client.send(CINF(filename=filename)).data_str
        Mediainfo = client.send(CINF(filename=filename)).data_str
        details = Mediainfo.split('"')
        mediadetails = details[2].split(' ') 
        mdetails = []
        for item in mediadetails:
            if item != '':
                mdetails.append(item)
        return mdetails
    except:
        # print("failed to retreve media details, using alternative method.")
        mdetails = []
        mediadetails = alt_get_media_details(filename)
        for item in mediadetails:
            if item != '':
                mdetails.append(item)
        return mdetails


def alt_get_media_details(filename): 
    try:
        media = client.send(CLS())
        media = client.send(CLS())
        media_list = media.data
        for line in media_list:
            medialine = line.split('"')
            if medialine[1] == filename:
                mediadetails = medialine[2].split(' ')
                # print("Alternative method sucessfull")
                return mediadetails
    except Exception as e:
        # print(e)
        # print("Alternative method failed")
        return ["","0","0","0","999999"]


# def media_legnth(filename, mediadetails):
#     # mediadetails = get_media_details(filename)
#     legnth = mediadetails[4]
#     return legnth

def load_settings():
    global settingsXML
    try:
        # settings = asyncio.new_event_loop().run_until_complete(client.send(DATA_RETRIEVE(name="Server_settings")))
        settings = client.send(DATA_RETRIEVE(name="Server_settings"))
        settingsXML = ET.fromstring(settings.data_str)
    except:
        settingsXML = ET.Element('settings')
        settingsXML.set('channels', '1')

        settingsXML.set('bible_splitLegnth', '45')
        settingsXML.set('bible_maxlines', '4')
        template = ET.SubElement(settingsXML,'template')
        preset = ET.SubElement(template,'preset')
        preset.set('name', 'bible')
        preset.text = ',,'
        print("Could not load server_settings")

def import_pro6_file(filename):
    try:
        import base64
        from striprtf.striprtf import rtf_to_text
    except Exception as e:
        print(e)

    try:
        parser6 = ET.XMLParser()
        XmlSongPath = filename
        song = ET.parse(XmlSongPath,parser6)
        pro6XML = song.getroot()
        print("Pro6 file loaded")
        load = True
    except:
        print("unable to load Pro6 File")
        pro6XML = None
        load = False

    if load == True:
        # loads the metadata
        NewSongXml = ET.Element('song')
        fname = filename.split("/")
        fname = fname[len(fname) -1]
        fname = fname.split('.')
        fname = replace_char(fname[0],' ', '_')
        APPapplication.songname = "/songs/" + fname

        selectedArrangementID = pro6XML.get("selectedArrangementID")
        category = pro6XML.get("category")
        notes = pro6XML.get("notes")
        CCLIAuthor = pro6XML.get("CCLIAuthor")
        CCLIArtistCredits = pro6XML.get("CCLIArtistCredits")
        CCLISongTitle = pro6XML.get("CCLISongTitle")
        CCLIPublisher = pro6XML.get("CCLIPublisher")
        CCLICopyrightYear = pro6XML.get("CCLICopyrightYear")
        CCLISongNumber = pro6XML.get("CCLISongNumber")

        NewSongXml.set('category',category)
        NewSongXml.set('notes',notes)
        NewSongXml.set('CCLIAuthor',CCLIAuthor)
        NewSongXml.set('CCLIArtistCredits',CCLIArtistCredits)
        NewSongXml.set('CCLISongTitle',CCLISongTitle)
        NewSongXml.set('CCLIPublisher',CCLIPublisher)
        NewSongXml.set('CCLICopyrightYear',CCLICopyrightYear)
        NewSongXml.set('CCLISongNumber',CCLISongNumber)
        # print(CCLISongTitle)
        # print(CCLIPublisher)
        # print(CCLICopyrightYear)
        # print(CCLISongNumber)
        
        verseindex = []# temporary lookup table of uuid and versename
        verseNameindex = []
        # versecnt = 0
        versea = ET.SubElement(NewSongXml, 'verse')
        
        for child in pro6XML:
            if child.get('rvXMLIvarName') == "groups":
                vcnt = 0
                for group in child:
                    verse = ET.SubElement(versea, 'verse')
                    vname = group.get("name")
                    verse.set('name',vname)
                    verse.set('id', str(vcnt))
                    vcnt += 1
                    color = group.get("color")
                    color.split()
                    color = list(map(float, color.split()))
                    cnt = 0
                    rgb = []
                    bg = "#"
                    for num in color:
                        if cnt == 3:
                            if num == 1:
                                fg = "white"
                            else:
                                fg = "black"
                        else:
                            num = int(round(num * 255))
                            hexcode = str(hex(num))
                            hexcode = hexcode[2:]
                            
                            if len(hexcode) == 1:
                                hexcode = "0" + hexcode

                            bg = bg + hexcode
                            rgb.append(num)
                            cnt+=1

                    uuid = group.get("uuid")
                    verseindex.append(uuid)
                    verseNameindex.append(vname)
                    scnt=0
                    for slidegroup in group:
                        if slidegroup.get('rvXMLIvarName') == "slides":
                            for slides in slidegroup:
                                slide = ET.SubElement(verse, 'slide')
                                slide.set('id', str(scnt))
                                scnt +=1
                                textinslide = False

                                hotkey = slides.get("hotKey")
                                if hotkey == None:
                                    hotkey = ""
                                slide.set('hotkey', hotkey)
                                verse.set('hotkey', hotkey)

                                notes = slides.get("notes")
                                if notes == None:
                                    notes = "\t"
                                slide.set('Header',notes)
                                slide.set('MediaName', "")
                                slide.set('REF', "")

                                for DisplaySlide in slides:
                                    try:
                                        if DisplaySlide.get('rvXMLIvarName') == "cues":
                                            timer = ""
                                            timerloop = ""
                                            for cues in  DisplaySlide:
                                                if cues.get('displayName') == "Go to Next":
                                                    timer = cues.get('duration')
                                                    timerloop = cues.get('loopToBeginning')
                                            slide.set("timer", timer)
                                            slide.set("timerloop", timerloop)
                                        slidetext = "\t"
                                        if DisplaySlide.get('rvXMLIvarName') == "displayElements":
                                            for displayElements in DisplaySlide:
                                                if displayElements.get('displayName') == "TextElement":
                                                    for rnvtext in displayElements:
                                                        if rnvtext.get("rvXMLIvarName") == "RTFData":
                                                            RTFData = rnvtext.text
                                                            rtf = base64.standard_b64decode(RTFData)
                                                            slidetext = rtf_to_text(rtf.decode())
                                        slide.text =  slidetext
                                    except:
                                        y=None
                    FGcolor = ET.SubElement(verse, 'FGcolor')
                    BGcolor = ET.SubElement(verse, 'BGcolor')
                    FGcolor.text = fg
                    BGcolor.text = bg
        proarangement = ""
        if child.get('rvXMLIvarName') == "arrangements":
            for arangements in child:
                name = arangements.get("name")            
                for itemId in arangements[0]:
                    for x in range(len(verseindex)):
                        if verseindex[x] == itemId.text:
                            if proarangement == "":
                                proarangement = str(x)
                            else:
                                proarangement = proarangement + ',' + str(x)

        arangement = ET.SubElement(NewSongXml, 'arangement')
        arangement.text = proarangement
        APPapplication.NewSongXml = NewSongXml
        APPapplication.choose_template("NewXml",NewSongXml,"")

def LoadBible(xml_bible_path):
    global BibleXML
    xml_bible_path = biblename
    try:
        parser = ET.XMLParser()
        Bible = ET.parse(xml_bible_path,parser)
        BibleXML = Bible.getroot()
        print("Bible loaded")
    except:
        print("unable to load Bible")
        BibleXML = None

def update_bible_list(): # function still in development
    global biblelistXml
    # global biblenameIndex
    # global biblenNameIndexFile
    # try:
    #     parser4 = ET.XMLParser()
    #     # biblepath
    #     XmlBiblePath = replace_char(os.getcwd(),'\\','/') + "/" + 'biblelist.xml'
    #     Biblelistx = ET.parse(xml_bible_path,parser4)
    #     biblelistXml = Biblelistx.getroot()
    #     print("Bible list loaded")
    # except:
    #     print("failed to load Bible list")
    #     # BibleXML = None
    #     biblelistXml = ET.Element(bibles)
    # biblenNameIndexFile = []
    # for entry in os.listdir(xml_bible_path):
    #     if os.path.isfile(os.path.join(basepath, entry)):
    #         try:
    #             if entry[-3:] == "xml":
    #                 success = False
    #                 for bible in biblelistXml:
    #                     if bible.text == entry:
    #                         success = True
    #                 if success == False:
    #                     LoadBible(xml_bible_path)
    #                     for info in BibleXML:
    #                         if info.tag == 'INFORMATION':
    #                             title = info.find('title')
    #                             identifier = info.find('identifier') 
    #                             language = info.find('language')
    #                             newbible = ET.SubElement('bible', biblelistXml)
    #                             newbible.text = title.text
    #                             newbible.set('identifier',identifier)
    #                             newbible.set('language',language)
    #                 biblelist.append(entry)
    #         biblenNameIndexFile.append(entry)
    # LoadBible(xml_bible_path)

def Test_code(event):
    # filename = "Another in the fire by Hillsong.pro6"
    print(event)
    # client.send(CHANNEL_GRID())

# def Rearange_verse(event):
#     if event.y <= -30 and event.y >= -100:
#         print("slide up")
#         sleep(1)
#     if event.y >= 100 and event.y <= 220:
#         print("slide down")
#         sleep(1)

def Fade_to_black(channels , layer):
    media_channels = channels.split('.')
    for channel in media_channels:
        client.send(PLAY(video_channel=int(channel), layer=layer, clip="#FF000000", transition="MIX", duration=18, frames=20 ))
        # PLAY(video_channel=channel, layer=layer, clip=MediaName, transition="MIX", loop='LOOP', duration=30, frame=seek, frames=legnth))

def reset_New_media_playing():
    global New_media_playing
    New_media_playing = True

def caspar_data_exist(filename):
    result = False
    List = client.send(DATA_LIST()).data
    for item in List:
        if item == filename:
            result = True
    return result


def clearKeys(event):
    global update_template
    global PauseState
    global enable_timer
    global Video_countdown
    channels = int(settingsXML.get('channels'))

    if event.keysym =='F1':
        enable_timer = False
        PauseState = True
        fade_enabled = False
        for x in range(1, channels + 1):
            client.send(CLEAR(video_channel=x))
            update_template[x - 1] = False
        print("Channel cleared")
    elif event.keysym == 'F2':
        enable_timer = False
        fade_enabled = False
        for x in range(1, channels + 1):
            update_template[x - 1] = False
            client.send(STOP(video_channel=x, layer=20))

    elif event.keysym =='F3':
        enable_timer = False
        fade_enabled = False
        for x in range(1, channels + 1):
            client.send(STOP(video_channel=x, layer=10))
        print("Media cleared")

    elif event.keysym =='F5':
        for x in range(1, channels + 1):
            client.send(STOP(video_channel=x, layer=30))

    elif event.keysym == 'F6':
        channel_range = range(1,channels)
        media_channels = List_to_CSV(channel_range, '.')
        Fade_to_black(media_channels ,10)

    elif event.keysym == 'F7':
        if Video_countdown == True:
            Video_countdown = False
            client.send(STOP(video_channel=channels, layer=21))
            print("Removing video countdown")
        else:
            Video_countdown = True
            Display_video_countdown()

    elif event.keysym == 'F8':
        if PauseState == False:
            PauseState = True
            for x in range(1,channels):
                client.send(PAUSE(video_channel=x, layer=5))
                print("Media on layer 5 Paused")
        else:
            PauseState = False
            for x in range(1,channels):
                client.send(RESUME(video_channel=x, layer=5))
                print("Media on layer 5 Resumed")
    elif event.keysym == 'F9':
        stream_channel(3,2)

def Send_next(event):
    channels = int(settingsXML.get('channels'))
    for x in range(1,channels + 1):
        client.send(CG_NEXT(video_channel=x, layer=20, cg_layer=20))
    print("Sending \"CG Next\" command")

def Display_video_countdown():
    channels = int(settingsXML.get('channels'))

    print("adding video countdown to channel: " + str(channels))
    data_xml = ET.Element('templateData')
    countdown_seconds = round(Video_Seconds - float("%s" % (time.time())))
    # countdown = countdown_seconds / 60
    # component_Element = ET.SubElement(data_xml, 'componentData')
    # component_Element.set('id','time')
    # dataValue = ET.SubElement(component_Element, 'data') 
    # dataValue.set('id', 'text')
    # dataValue.set('value', str(countdown_seconds))
    # Template = "scene/stage/Stage_countdown"
    # template_data_str = ET.tostring(element=data_xml, encoding='unicode')
    data_xml = ET.Element('templateData')
    component_Element = ET.SubElement(data_xml, 'componentData')
    component_Element.set('id', "countdown")
    dataValue = ET.SubElement(component_Element, 'data') 
    dataValue.set('id', 'text')
    dataValue.set('value', str(countdown_seconds / 60))
    template_data_str = ET.tostring(element=data_xml, encoding='unicode')
    # client.send(CG_UPDATE)

    # client.send(CG_UPDATE(video_channel=channels, layer=20, cg_layer=20, data=template_data_str))

    client.send(CG_ADD(video_channel=channels, layer=21, cg_layer=21, template="CHURCH/STAGE_COUNTDOWN/INDEX", play_on_load=1, data=template_data_str))

def SlideNav(event):
    global VerseLineBtnIndex
    global enable_timer
    enable_timer = True
    # print(event)   # leave in, for debugging only

    if Enable_pres_remote == True:
        if event.keysym == 'Prior':
            Action = "Prev"
        if event.keysym == 'Next':
            Action = "Next"

    if event.keysym == 'Right':
        Action = "Prev"
    if event.keysym == 'Left':
        Action = "Next"


    if  Action == "Prev":
        if (VerseLineBtnIndex + 1) <= (VerseLineBtnCnt -1):
            VerseLineBtnIndex += 1   
            Send_Verse(VerseLineBtnIndex)
            verseline_button_indicator()
    if Action == "Next":
        if (VerseLineBtnIndex - 1) >= 0:
            VerseLineBtnIndex -= 1     
            Send_Verse(VerseLineBtnIndex)
            verseline_button_indicator()

    for x in range(len(VerseHotkey)):
        if event.keysym == VerseHotkey[x]:
            VerseLineBtnIndex = VerseHotkeyIndex[x]
            Send_Verse(VerseLineBtnIndex)
            verseline_button_indicator()
    
def RundownNav(event):
    if event.keysym == 'Up':
        check_rundown_item("Up")
    if event.keysym == "Down":
        check_rundown_item("Down")
    
def Load_Rundown(filename):
    global RunDownXML
    global Rundown_name
    global RundownItemCnt
    global RundownItemCurrent
    global RundownItemRow
    global RundownItemThumbnail
    global RundownThumbnailIndex
    global rundownItemLast
    global RundownItemPos_index

    RundownItemPos_index = 0
    RundownItemRow=0
    try:    #sets RundownItemCnt to zero only if rundown xml is loaded for the first time
        x=RundownItemCnt
    except:
        RundownItemCnt = 0
    APPapplication.Rundown_grid.configure(height=0)

    # RundownItemCurrent = 0
    rundownItemLast = -1
    RundownItemCommandIndex = []
    RundownItemThumbnail = []
    RundownThumbnailIndex = [] 

    Rundown_name = filename
    APPapplication.Clear_rundown()
    RundownItemCurrent = -1
    parser1 = ET.XMLParser()
    cnt = 0
    if caspar_data_exist(filename) == True:
        while cnt <= 20:
            try:       # Retreving the rundown twice is intentional overcomes plugin bug    
                rundownlist = client.send(DATA_RETRIEVE(name=filename))
                rundownlist = client.send(DATA_RETRIEVE(name=filename))
                rundownlist = client.send(DATA_RETRIEVE(name=filename))
                rundownlist = client.send(DATA_RETRIEVE(name=filename))
                RunDownXML = ET.fromstring(rundownlist.data_str)
                cnt = 20
                print("Rundown loaded")
                
            except:
                RunDownXML = ET.Element('RunDown')
                print("Rundown failed to load")
            cnt += 1
    else:
        RunDownXML = ET.Element('RunDown')
        print("Rundown not found!")
    Fill_Rundown()


def Fill_Rundown():
    global RundownItemCnt
    for item in RunDownXML:
        bgcolor = item.get('bgcolor')
        Name = item.text
        Index = item.get('id')
        Type = item.get('Type')
        medianame = item.get('medianame')

        if medianame != None:
            mediaType = item.get('selected_mediatype')
            if mediaType == "AUDIO":
                photo = ""
            else:
                photo = medianame
        else:
            photo = "" 
        
        if Type == "Song":
            command = item.get('Songname')
        if Type == "Media":
            command = []
            command.append(item.get('medianame'))
            command.append(item.get('selected_mediatype'))
            command.append(item.get('channel'))
            command.append(item.get('layer'))
            command.append(item.get('looping'))
            command.append(item.get('fade'))
            command.append(item.get('seek'))
            command.append(item.get('legnth'))
            command.append(item.get('transition'))
            command.append(item.get('duration'))
            command.append(item.get('direction'))
            command.append(item.get('tween'))
            title = item.get('Title')
            if title == None:
                title = medianame
            command.append(title)

        APPapplication.add_rundown_button(bgcolor, Name, RundownItemCnt, photo, False, Type, command)
        RundownItemCnt += 1

    print("Rundown loaded sucessfully")

def UseRundownItem(index):
    global RundownItemCurrent
    global rundownItemLast
    global Rundown_Item_Frame
    
    RundownItemCurrent = int(index)

    for item in RundownItemFrame:
        if item.Position_index == RundownItemCurrent:
            CurrentButton = item.button
            command = item.command
            Type = item.Type

        if item.Position_index == rundownItemLast:
            LastButton = item.button
    try:
        Last_rundown_item_fgcolor = LastButton.cget('fg')
        Last_rundown_item_bgcolor = LastButton.cget('bg')
        LastButton.configure(fg=Last_rundown_item_bgcolor, bg=Last_rundown_item_fgcolor)
    except:
        y = None

    current_rundown_item_fgcolor = CurrentButton.cget('fg')
    current_rundown_item_bgcolor = CurrentButton.cget('bg')
    CurrentButton.configure(fg=current_rundown_item_bgcolor, bg=current_rundown_item_fgcolor)
    rundownItemLast = RundownItemCurrent

    if Type == "Song":
        APPapplication.Load_song(command)

    if Type == "Media":
        medianame = command[0]
        selected_mediatype = command[1]
        Media_channels = command[2]
        layer = command[3]
        transition = command[8]
        duration = command[9]
        direction = command[10]
        tween = command[11]
        looping =  command[4]
        looping = string_to_bool(looping)

        if selected_mediatype == "MOVIE":
            fade =  command[5]
            fade = string_to_bool(fade)
            legnth = command[7]
            seek = command[6]

            if legnth == "0":
                m_details = get_media_details(medianame)
                # legnth = media_legnth(medianame, m_details)
                legnth = m_details[3]
            if fade == True:
                Fade_to_black(Media_channels,int(layer))
                sleep(1)
                
        else:
            looping = False
            fade = False
            legnth = "0"
            seek = "0"

        Media_channels = Media_channels.split('.')

        for channel in Media_channels:
            channel = int(channel)
            # print(seek)
            # print("legnth" + str(legnth))
            # print(duration)
            # print(medianame, selected_mediatype, int(channel), int(layer), looping, int(seek), int(legnth), fade,  transition, int(duration), direction, tween)
            PlayMediaFile(medianame, selected_mediatype, int(channel), int(layer), looping, int(seek), int(legnth), fade,  transition, int(duration), direction, tween)

def check_rundown_item(direction):
    global RundownItemCurrent
    if direction == "Up":
        if RundownItemCurrent >= 1:
            end1 = False
            x = RundownItemCurrent
            while end1 == False:
                x -= 1
                for index in RundownItemFrame:
                    if index.Position_index == x:
                        if index.state == True:
                            end1 = True
                            RundownItemCurrent -= 1
                            UseRundownItem(x)
    if direction == "Down":
        #possible bug?
        if RundownItemCurrent <= RundownItemCnt:
            end1 = False
            x = RundownItemCurrent
            while end1 == False:
                x += 1
                for index in RundownItemFrame:
                    if index.Position_index == x:
                        if index.state == True:
                            end1 = True
                            RundownItemCurrent += 1
                            UseRundownItem(x)

def use_Verse_profile(event):
    global new_fgcolor
    global new_bgcolor
    verse_profile = APPapplication.verse_profiles_listbox.get(ACTIVE)
    APPapplication.new_verse_name.delete(0,END)
    APPapplication.new_verse_name.insert(END,verse_profile)

    for Verse in settingsXML:
        if Verse.tag == "verse":
            for profile in Verse:
                if profile.get('name') == verse_profile:
                    colors = profile.text
    
    color = colors.split(',')
    new_fgcolor = color[0]
    new_bgcolor = color[1]
    APPapplication.sample_button.configure(bg=new_bgcolor,fg=new_fgcolor)

def KEY_bible_verse(event):
    global bibleVersebtnCurrent
    if event.keysym == 'Right':
        if (bibleVersebtnCurrent + 1) <= (BibleverseBtnCnt -1):
            bibleVersebtnCurrent += 1   
            Send_bible_verse_caspar(bibleVersebtnCurrent)
    if event.keysym == 'Left':
        if (bibleVersebtnCurrent - 1) >= 0:
            bibleVersebtnCurrent -= 1     
            Send_bible_verse_caspar(bibleVersebtnCurrent)

def Send_bible_verse_caspar(index):
    global bibleVersebtnindex
    global bibleVersebtnOld
    channels = int(settingsXML.get('channels'))
    number_lines_to_send = int(settingsXML.get('bible_maxlines'))
    BibleText = bibleVerseIndex[index]
    try:
        bibleVersebtnindex[bibleVersebtnOld].configure(bg="blue")
        bibleVersebtnindex[bibleVersebtnOld].configure(fg="white")
    except:
        y=None
    try:
        bibleVersebtnindex[index].configure(bg="white")
        bibleVersebtnindex[index].configure(fg="blue")
    except:
        y=None
    bibleVersebtnOld = index
    dataNames = []
    datacnt = 0
    data = BibleText.split('\n')
    for item in settingsXML:
        if item.tag == "template":
            for preset in item:
                if preset.get('name') == "Bible":
                    template = preset.text
    try:
        template = template.split(',')
    except:
        y=None
    template_list = []
    for x in range(0, channels):
        try:
            template_list.append(template[x])
        except:
            template_list.append("")

    for x in range(len(data)):
        dataNames.append('f' + str(datacnt)) 
        datacnt += 1
    y = len(data)
    x = False 
    while x == False:
        if y <= numLinesToSend:
            data.append("") # appends the remaining fields with nothing 
            y += 1
            dataNames.append('f' + str(datacnt))
            datacnt += 1
        else:
            x = True
    try:
        BibleTextB = bibleVerseIndex[index + 1]
        second_slide = True
    except:
        second_slide = False
    if second_slide == True:    # begin next slide data f (fields only)
        BibleTextB = BibleTextB.split(',')
        for x in range(0,number_lines_to_send):
            try:
                data.append(BibleTextB[x])
                dataNames.append('b' + str(x))
            except:
                data.append("")
                dataNames.append('b' + str(x))
    if second_slide == False:
        for x in range(0,number_lines_to_send):
            data.append("")
            dataNames.append('b' + str(x))    # end next slide data

    dataNames.append("ref") # hendles the bible verse reference
    data.append(bibleVerseIndexREF[index])
    print("template_list" + str(template_list))
    use_template(20,20,template_list,data,dataNames)

def verseline_button_indicator():   # swaps the fg and bg color on the current slide button.
    global VerseLineBtnIndex
    global VerseLineBtnIndexLast
    global last_BG
    global last_FG
    # VerselineButton[VerseLineBtnIndex].configure(highlightbackground='red')
    if VerseLineBtnIndexLast != VerseLineBtnIndex:
        if last_BG != "First": # last_BG = "First"
            VerselineButton[VerseLineBtnIndexLast].configure(bg=last_BG)
            VerselineButton[VerseLineBtnIndexLast].configure(fg=last_FG)
        last_BG = VerselineButton[VerseLineBtnIndex].cget('bg')
        last_FG = VerselineButton[VerseLineBtnIndex].cget('fg')
        VerselineButton[VerseLineBtnIndex].configure(bg=last_FG)
        VerselineButton[VerseLineBtnIndex].configure(fg=last_BG)
        VerseLineBtnIndexLast = VerseLineBtnIndex

def Send_Verse(index): # retreves the current slide from songxml and uses the use_template function to display text also uses the PlayMediaFile function to play media
    global LastTemplate
    number_lines_to_send = int(settingsXML.get('bible_maxlines'))
    channels = int(settingsXML.get('channels'))
    verse_slide = VerseText[index]
    verse_slide = verse_slide.split(',')
    Verse_id = verse_slide[0]
    Slide_id = verse_slide[1]
    try:
        verse_slide2 = VerseText[index + 1]
        verse_slide2 = verse_slide2.split(',')
        Verse_id2 = verse_slide2[0]
        Slide_id2 = verse_slide2[1]
        second_slide = True
    except:
        second_slide = False

    for verse_element in songxml:
        for verse_Name in verse_element:
            if verse_Name.get("id") == Verse_id:
                for Slide in verse_Name:
                    if Slide.get("id") == Slide_id:
                        Slide1 = Slide
            if second_slide == True:             
                if verse_Name.get("id") == Verse_id2:
                    for Slide in verse_Name:
                        if Slide.get("id") == Slide_id2:
                            verseB = Slide.text 
                       
    Versetext = Slide1.text
    template = Slide1.get("template")
    MediaName = Slide1.get("MediaName")
    timer = Slide1.get("timer")
    try: # remove line from final version
        if timer =="":
            timer = 0
        else:
            timer = int(timer)
    except:# remove line from final version
        timer = 0# remove line from final version

    header = Slide1.get("Header")
    REF = Slide1.get("REF")

    # Media parseing section
    if MediaName != "":
        channel = Slide1.get("channel")
        mediaType = Slide1.get("mediaType")
        layer = Slide1.get("layer")
        loop = Slide1.get("looping")
        loop = string_to_bool(loop)
        fade = Slide1.get("fade")
        fade = string_to_bool(fade)
        seek = Slide1.get("seek")
        legnth = Slide1.get("legnth")  
        transition = Slide1.get("transition")
        duration = Slide1.get("duration")
        direction = Slide1.get("direction")
        tween = Slide1.get("tween")

        if legnth == "0":   
            if mediaType == "MOVIE":
                Mediainfo = client.send(CINF(filename=MediaName)).data_str
                details = Mediainfo.split('"')
                mediadetails = details[2].split(' ') 
                legnth = mediadetails[4]

        if fade == True:
            Fade_to_black(channel,int(layer))
            sleep(.5)
        Media_channels = channel.split('.')

        for channel in Media_channels:
            PlayMediaFile(MediaName, mediaType, int(channel), int(layer), loop, int(seek), int(legnth), fade, transition, int(duration), direction, tween) 
        #  end media parseing section

    template_list = template.split(',')
    if len(template_list) <= channels:
        for x in range(channels - 1):
            template_list.append("")
    cnt = 1
    
    # creates last template if it doesent exist already
    try:
        x=LastTemplate
    except:
        for x in range(channels - 1):
            LastTemplate.append("")
    for x in range(len(LastTemplate)):
        if template_list[x] != LastTemplate[x]: 
            update_template = True
            clear_channel(x + 1, 20,1)
            LastTemplate[x] = template_list[x]

    # attempts to split the verse into multiple lines if it fails a blank second line is added
    verse = []
    Versetext = Versetext.split('\n')
    verseId = []

    for x in range(0,number_lines_to_send):
        try:
            verse.append(Versetext[x])
        except:
            verse.append("")
        verseId.append("f" + str(x))

    # clears channels if slide is blank, tab "\t" is used as a control character
    if verse[0] == "\t":
        for x in range(0,channels -1):
            template_list[x] = ""
    try:
        if header != '\t':
            header = header.split('[---]')
            for x in range(len(header)):
                verse.append(header[x])
                verseId.append('h' + str(x))
    except:
        y=None

    if REF == None: # remove line from final version
        REF = "" # remove line from final version
    try:
        if REF != "":
            verse.append(REF)
            verseId.append("ref")
    except:
        y=None

    if second_slide == True:    # begin next slide data f (fields only) stored as b fields
        verseB = verseB.split('\n')
        for x in range(0,number_lines_to_send):
            try:
                verse.append(verseB[x])
                verseId.append('b' + str(x))
            except:
                verse.append("")
                verseId.append('b' + str(x))
    if second_slide == False:
        for x in range(0,number_lines_to_send):
            verse.append("")
            verseId.append('b' + str(x))    # end next slide data

    use_template(20, 1, template_list, verse, verseId)
    
    if timer != 0:  # activates the slide autoplay
        APPapplication.after(timer * 1000, slide_advance_timer)



def slide_advance_timer():
    global VerseLineBtnIndex
    if enable_timer == True:
        if (VerseLineBtnIndex + 1) <= (VerseLineBtnCnt -1):
            VerseLineBtnIndex += 1   
            Send_Verse(VerseLineBtnIndex)
            verseline_button_indicator()
        elif (VerseLineBtnIndex + 1) == (VerseLineBtnCnt -1):
            VerseLineBtnIndex = 0
            Send_Verse(VerseLineBtnIndex)
            verseline_button_indicator()

def caspar_info(event): # test function, no practical use
    # print(client.send(INFO_QUEUES()))
    # print(client.send(HELP_CONSUMER(consumer="STREAM")))
    # print(client.send(HELP_PRODUCER()))
    print(client.send(HELP()))
    #  print(client.send(CG_INFO(video_channel=1)).data)

    # HELP_CONSUMER,HELP,HELP_PRODUCER
    # print(client.send(INFO(video_channel=0,layer=5)))

def clear_channel(channel, video_layer, layer):
    update_template[channel - 1] = False
    client.send(CG_STOP(video_channel=channel, layer=video_layer, cg_layer=layer))

    
def PlayMediaFile(MediaName, MediaType, channel, layer, loop, seek, legnth, fade, transition, duration, direction, tween):
    global Video_countdown
    global Video_Seconds
    global New_media_playing
    print("Play :", MediaName, MediaType, channel, layer, loop, seek, legnth)
    print("channel : " +str(channel))
    print("layer : " +str(layer))
    print("loop : " ,loop)
    print("fade : " ,fade)
    print("seek : " +str(seek))
    print("legnth : " +str(legnth))
    print("fade :" ,fade)
    print("transition :" ,transition)
    print("duration :" ,duration)
    print("direction :" ,direction)
    print("tween :" ,tween)

    channels = int(settingsXML.get('channels'))

    if New_media_playing == True:
        New_media_playing = False
        APPapplication.after(2000, reset_New_media_playing)

        if MediaType == "MOVIE": 
            m_details = get_media_details(MediaName)
            if legnth == 999999999 or legnth == 0:
                Seconds = media_seconds(MediaName, 0, m_details) 
                # legnth = int(media_legnth(MediaName, m_details))
                legnth = int(m_details[3])
            else:
                Seconds = round(media_seconds(MediaName, legnth, m_details))
            # except:
                # Seconds = 2 # Resets the video timer to 2 in the case that the CINF command fails I.E. no video countdown
            if loop == False:   # only displays video countdown if loop is false 
                Video_Seconds = round(float("%s" % (time.time() + Seconds)))
                if Video_countdown == True:
                    Display_video_countdown()
    
    if MediaType == "MOVIE":
        Seek=seek
        Legnth=legnth
    else:
        Seek = None
        Legnth = None

    if loop == True:
        client.send(PLAY(video_channel=channel, layer=layer, clip=MediaName, transition=transition, loop='LOOP', duration=duration, frame=seek, frames=legnth, direction=direction, tween=tween))
    else:
        client.send(PLAY(video_channel=channel, layer=layer, clip=MediaName, transition=transition, duration=duration, frame=seek, frames=legnth, direction=direction, tween=tween))
        # if MediaType == "MOVIE":# This function updates the stage display with the video countdown 
            
                
    if fade == True:
        client.send(LOADBG(channel=int(channel), layer=int(layer), clip="#FF000000", transition="MIX", duration=18, frames=60))
        # client.send(LOADBG(channel=1, layer=10, clip="#FF000000", transition="MIX", duration=18, frames=60, auto='AUTO'))

def use_template(video_layer, layer, Template, data, dataName):
    channels = int(settingsXML.get('channels'))
    data_xml = ET.Element('templateData')

    for x in range(len(data)):
        component_Element = ET.SubElement(data_xml, 'componentData')
        component_Element.set('id', dataName[x])
        dataValue = ET.SubElement(component_Element, 'data') 
        dataValue.set('id', 'text')
        dataValue.set('value', data[x])
    
    template_data_str = ET.tostring(element=data_xml, encoding='unicode')
    client.send(DATA_STORE(name="current_data", data=template_data_str))

    for x in range(1,channels + 1):
        if Template[x - 1] != "":
            if update_template[x-1] == False:
                update_template[x-1] = True
                client.send(CG_ADD(video_channel=x, layer=video_layer, cg_layer=layer, template=Template[x - 1], play_on_load=1, data="current_data"))
            else:
                client.send(CG_UPDATE(video_channel=x, layer=video_layer, cg_layer=layer, data="current_data"))
        else:
            clear_channel(x, 20, 1)
####################### end of caspar functions

client = Client()
def load_client_settings():
    global biblename
    global Server_Ip
    global Server_port
    global ClientSettingsXML
    try:
        parser3 = ET.XMLParser()
        XmlPath = replace_char(os.getcwd(),'\\','/') + "/" + "client_settings.xml"
        clientsettings = ET.parse(XmlPath,parser3)
        ClientSettingsXML = clientsettings.getroot()
        print("Client_settings_loaded")

    except:
        ClientSettingsXML = ET.Element('settings')
        bible = ET.SubElement(ClientSettingsXML,'bible')
        ip = ET.SubElement(ClientSettingsXML,'server_ip')
        port = ET.SubElement(ClientSettingsXML,'server_port')

        bible.text = "*" #"SF_2009-01-23_ENG_KJV_(KING_JAMES_VERSION).xml"
        ip.text = "127.0.0.1"
        port.text = "5250"

        print("unable to load \"client_settings.xml\"")

    biblename = ClientSettingsXML[0].text
    if biblename == "*":
        biblename = ""
    Server_Ip = ClientSettingsXML[1].text
    Server_port = int(ClientSettingsXML[2].text)

def connect_to_caspar():
    global Connected
    try:
        Connected = True
        # print("trying")
        client.connect(Server_Ip, Server_port)  # defaults to 127.0.0.1, 5250
    # client = ClientAsync()
    # asyncio.new_event_loop().run_until_complete(client.connect(Server_Ip, Server_port))
        # client_async = ClientAsync()
        # asyncio.new_event_loop().run_until_complete(client_async.connect(Server_Ip, Server_port))
        print("connected to a CasparCG server at:   " + str(Server_Ip) + " port: " + str(Server_port))
    except:#3.0
        Connected = False
        print("could not contact server!")
load_client_settings()
connect_to_caspar()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        # self.configure(width=1920,height=1080)
        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(root, 0, weight=1)

        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(root, 1, weight=1)


        self.Load_master()

        master.bind('<Left>', SlideNav)
        master.bind('<Right>', SlideNav)
        master.bind('<Prior>', SlideNav)
        master.bind('<Next>', SlideNav)

        master.bind('<Up>', RundownNav)
        master.bind('<Down>',RundownNav)

        master.bind('<F1>', clearKeys)
        master.bind('<F2>', clearKeys)
        master.bind('<F3>', clearKeys)
        master.bind('<F4>', clearKeys)
        master.bind('<F5>', clearKeys)
        master.bind('<F6>', clearKeys)
        master.bind('<F7>', clearKeys)
        master.bind('<F8>', clearKeys)
        master.bind('<F9>', clearKeys)

        master.bind('<F10>', Send_next)
        master.bind('<F11>', caspar_info)
        master.bind('<F12>', Test_code)
        master.bind('<Alt-b>', launch_bible)
        # master.bind('<Configure>', Rezize_frames)
        # master.bind('<Enter>', Resize_framesB)

        master.title("CasparCG Church 1.2.1")

    def Load_master(self):
        global update_template
        global Video_countdown
        global New_media_playing
        global RundownItemFrame
        global Video_Seconds
        global fade_channels
        global fade_enabled

        global ThumbnailIndex
        global ThumbnailNameIndex
        global ThumbnailsampleIndex

        global APPapplication
        global PauseState
        global Enable_pres_remote

        Enable_pres_remote = False  
        PauseState = False
        Video_countdown = False
        New_media_playing = True
        APPapplication = self
        Video_Seconds = 0
        fade_channels = ""
        fade_enabled = False
        self.standard_buttons_frame = tk.LabelFrame(self)
        self.standard_buttons_frame.grid(column=0,row=0)

        self.loadbibleBtn = tk.Button(self.standard_buttons_frame, text="Settings", command=self.Edit_settings).grid(column=1,row=0)

        self.add_to_Rundown_button = tk.Button(self.standard_buttons_frame, text="Add song to rundown", command=lambda x1="Rundown",x2=-1:self.choose_song(x1,x2)).grid(column=2,row=0)

        self.add_media_to_rundown_button = tk.Button(self.standard_buttons_frame, text="Add media to rundown", command= lambda x1="rundown",x2=-1:self.choose_media(x1,x2)).grid(column=3,row=0)
        self.add_bible_Verse_button = tk.Button(self.standard_buttons_frame, text="Add Bible Verse", command=self.load_bible).grid(column=0,row=0)

        self.open_song = tk.Button(self.standard_buttons_frame, text="Open Song", command= lambda x1="Open",x2=-1:self.choose_song(x1,x2)).grid(column=2,row=1)

        self.new_song_button = tk.Button(self.standard_buttons_frame, text="Create new song", command=self.create_new_song).grid(column=3,row=1)

        self.Clear_rundown_button = tk.Button(self.standard_buttons_frame, text="Clear_rundown", command=self.Clear_rundown).grid(column=0,row=1)
        self.Save_rundown_button = tk.Button(self.standard_buttons_frame, text="Save rundown", command=self.Save_rundown).grid(column=1,row=1)
        self.refresh_rundown_button = tk.Button(self.standard_buttons_frame, text="Refresh rundown", command=self.refesh_rundown).grid(column=1,row=2)
        self.toggle_pres_remote_button = tk.Button(self.standard_buttons_frame,text="Presentation Remote\ndisabled",bg="red",fg="white",command=self.toggle_pres_remote)
        self.toggle_pres_remote_button.grid(column=0,row=2)

        # begin rundown frame
        Rundown_frame = tk.LabelFrame(self)
        Rundown_frame.grid(column=0,row=1, sticky="nsew")#codechange11
        
        SC_canvas = add_scrollable_canvas(Rundown_frame , "Y", APPapplication, Width=540,G_Width=540)#, )#codechange11
        self.Rundown_canvas = SC_canvas[0]
        self.Rundown_grid = SC_canvas[1]

        # begin slide document(or song) frame 
        self.Slide_document_frame = tk.LabelFrame(self, text="No Document")
        self.Slide_document_frame.grid(column=1,row=1, sticky='nsw')#codechange11

        self.Slide_document_canvas = Canvas(self.Slide_document_frame,width=1300, height=900)#)#codechange11
        self.Slide_document_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # end song frame

        # begin Editsong Frame
        self.editverse = tk.LabelFrame(self,text="Edit Document",height=70,width=90)#height=70,width=90#codechange11
        self.editverse.grid(column=1,row=0, sticky="nsew")#codechange11

        self.Add_Verse_button = tk.Button(self.editverse, text="Add new verse", command= lambda x1="N", x2="white", x3="black":self.new_verse(x1,x2,x3)).grid(column=0,row=0)
        self.edit_arangement = tk.Button(self.editverse, text="Edit arangement", command=lambda x1=False:self.EditArangement(x1)).grid(column=1,row=0)
        self.change_Template_button = tk.Button(self.editverse, text="Change Default Template", command=lambda x1="Xml",x2="",x3="":self.choose_template(x1,x2,x3)).grid(column=2,row=0)
        # end frame definitions

        RundownItemFrame = []
        ThumbnailIndex = []
        ThumbnailNameIndex = []
        ThumbnailsampleIndex = []
        LoadBible(biblename)
        if Connected == True:
            load_settings()
            channels = int(settingsXML.get('channels'))
            update_template = []
            for x in range(channels):
                update_template.append(False)
            self.Update_thumbnail_index()
            Load_Rundown("RUNDOWN")

    def toggle_pres_remote(self):
        global Enable_pres_remote
        if Enable_pres_remote == True:
            self.toggle_pres_remote_button.configure(bg="red")
            self.toggle_pres_remote_button.configure(text="Presentation Remote\nDisabled")
            Enable_pres_remote = False
            print("presentation remote disabled")
        elif Enable_pres_remote == False:
            self.toggle_pres_remote_button.configure(bg="green")
            self.toggle_pres_remote_button.configure(text="Presentation Remote\nEnabled")
            Enable_pres_remote = True
            print("presentation remote enabled")

##################################### start of server config section

    def Edit_settings(self):
        global server_template_preset_index
        global server_template_preset_Frame
        global server_template_preset_status
        global server_template_preset_Name
        global server_template_preset_Count

        global server_Verse_profile_index
        global server_Verse_profile_Frame
        global server_Verse_profile_status
        global server_Verse_profile_Name
        global server_Verse_profile_Count

        server_template_preset_index = []
        server_template_preset_status = []
        server_template_preset_Frame = []
        server_template_preset_Name = []
        server_template_preset_Count = 0

        server_Verse_profile_index = []
        server_Verse_profile_Frame = []
        server_Verse_profile_status = []
        server_Verse_profile_Name = []
        server_Verse_profile_Count = 0

        self.Edit_server_config_frm = tk.Tk()

        Ip_address_label = tk.Label(self.Edit_server_config_frm,text="Server Ip:").grid(column=0,row=0)
        self.Ip_address_entry = tk.Entry(self.Edit_server_config_frm)
        self.Ip_address_entry.grid(column=0,row=1)

        Port_label = tk.Label(self.Edit_server_config_frm,text="Server port:").grid(column=1,row=0)
        self.Port_entry = tk.Entry(self.Edit_server_config_frm)
        self.Port_entry.grid(column=1,row=1)

        self.bible_folder_button = tk.Button(self.Edit_server_config_frm,text="Select Bible path",command=self.select_bible_path).grid(column=2,row=0)

        self.biblename_entry = tk.Entry(self.Edit_server_config_frm)
        self.biblename_entry.grid(column=2,row=1)

        self.biblename_entry.insert(END,biblename)

        self.Ip_address_entry.insert(END,Server_Ip)
        self.Port_entry.insert(END,Server_port)

        self.Edit_server_config_save_btn = tk.Button(self.Edit_server_config_frm,text="Save Settings",command=self.Save_server_config).grid(column=2,row=6)

        if Connected == True:
            channels = settingsXML.get('channels')   
        
            self.Edit_server_Config_add_preset = tk.Button(self.Edit_server_config_frm, text="Add Template Preset",command=lambda x1=None,x2="untitled":self.add_template_preset(x1,x2)).grid(column=0,row=6)
            self.Edit_server_Config_add_profile = tk.Button(self.Edit_server_config_frm, text="Add Verse Profile",command=lambda x1=["white","Black"],x2="untitled":self.add_Verse_profile(x1,x2)).grid(column=1,row=6)
            
            self.settings_preset_profileframe = tk.LabelFrame(self.Edit_server_config_frm)
            self.settings_preset_profileframe.grid(column=0,row=7, columnspan=3)

            # begin scrolling frame for Template Presets
            self.Edit_server_Template_preset_frame = tk.LabelFrame(self.settings_preset_profileframe)
            self.Edit_server_Template_preset_frame.grid(column=0,row=7,sticky="NSEW")

            SC_canvas = add_scrollable_canvas(self.Edit_server_Template_preset_frame , "Y", APPapplication, Height=800,Width=300,G_Width=200,G_Height=100)
            self.Edit_server_Template_preset_canvas = SC_canvas[0]
            self.Edit_server_Template_preset_grid = SC_canvas[1]

            # begin scrolling frame for Verse Profiles
            self.Edit_server_Verse_profiles_frame = tk.LabelFrame(self.settings_preset_profileframe)
            self.Edit_server_Verse_profiles_frame.grid(column=1,row=7,sticky="NSEW")

            SC_canvas = add_scrollable_canvas(self.Edit_server_Verse_profiles_frame , "Y", APPapplication, Height=800,Width=300,G_Width=200,G_Height=100)
            self.Edit_server_Verse_profiles_canvas = SC_canvas[0]
            self.Edit_server_Verse_profiles_grid = SC_canvas[1]


            self.Edit_server_channels_label = tk.Label(self.Edit_server_config_frm,text="please enter the number of channels").grid(column=0,row=4)
            self.Edit_server_channels = tk.Entry(self.Edit_server_config_frm)
            self.Edit_server_channels.grid(column=0,row=5)
            self.Edit_server_channels.insert(END,channels)

            label1 = tk.Label(self.Edit_server_config_frm,text="Bible, Max line legnth").grid(column=1,row=4)
            self.Edit_server_Bible_splitLegnth = tk.Entry(self.Edit_server_config_frm)
            self.Edit_server_Bible_splitLegnth.grid(column=1,row=5)

            label2 = tk.Label(self.Edit_server_config_frm,text="Bible, Max lines per slide").grid(column=2,row=4)
            self.Edit_server_Bible_Max_lines = tk.Entry(self.Edit_server_config_frm)
            self.Edit_server_Bible_Max_lines.grid(column=2,row=5)


            self.Edit_server_Bible_splitLegnth.insert(END,settingsXML.get('bible_splitLegnth'))
            self.Edit_server_Bible_Max_lines.insert(END,settingsXML.get('bible_maxlines'))

            BiblePreset = False
            for templatePresets in settingsXML:
                if templatePresets.tag == "template":
                    for Preset in templatePresets:
                        presetName = Preset.get('name')
                        template_list = Preset.text
                        template_list = template_list.split(',')
                        self.add_template_preset(template_list,presetName)
                        if presetName == "Bible":
                            BiblePreset = True
            if BiblePreset == False:
                self.add_template_preset(['','',''],"Bible")
            
            for verse_profile in settingsXML:
                if verse_profile.tag == "verse":
                    for profile in verse_profile:
                        profileName = profile.get('name')
                        Colors = profile.text
                        Colors = Colors.split(',')
                        self.add_Verse_profile(Colors,profileName)
                        Profiles_exist = True
                        
    def select_bible_path(self):
        biblepath = fd.askopenfilename()
        self.biblename_entry.insert(END,biblepath)


    def Pick_verse_color(self,index,Type, destination): # janky function
        global new_fgcolor
        global new_bgcolor

        if Type == "fg":
            fgcolor = colorchooser.askcolor()
            new_fgcolor = fgcolor[1]
            if destination =="Slides":
                self.foreground_color_button.configure(fg=new_fgcolor)
                self.sample_button.configure(fg=new_fgcolor)
            if destination == "Profile":
                server_Verse_profile_index[index].configure(fg=fgcolor[1])
            
        if Type == "bg":
            bgcolor = colorchooser.askcolor()
            new_bgcolor = bgcolor[1]
            if destination =="Slides":
                self.background_color_button.configure(bg=new_bgcolor)
                self.sample_button.configure(bg=new_bgcolor)
            if destination == "Profile":
                server_Verse_profile_index[index].configure(bg=bgcolor[1])

    def add_Verse_profile(self,Colors,Name):
        fgcolor = Colors[0]
        bgcolor = Colors[1]
        global server_Verse_profile_Count

        self.Edit_Verse_profile_frame = tk.LabelFrame(self.Edit_server_Verse_profiles_grid)
        self.Edit_Verse_profile_frame.pack()
        server_Verse_profile_Frame.append(self.Edit_Verse_profile_frame)
        self.Edit_Verse_profile_frame.Canvas = self.Edit_server_Verse_profiles_canvas # for mousewheel

        self.Edit_Verse_profile_color_sample_btn = tk.Button(self.Edit_Verse_profile_frame, fg=fgcolor ,bg=bgcolor, text="Sample")
        self.Edit_Verse_profile_color_sample_btn.grid(column=4,row=1)
        server_Verse_profile_index.append(self.Edit_Verse_profile_color_sample_btn)
        self.Edit_Verse_profile_color_sample_btn.Canvas = self.Edit_server_Verse_profiles_canvas # for mousewheel
        
        self.Edit_Verse_profile_background_color_btn = tk.Button(self.Edit_Verse_profile_frame,bg="red",text="background color",command = lambda x1=server_Verse_profile_Count,x2="bg",x3="Profile":self.Pick_verse_color(x1,x2,x3))
        self.Edit_Verse_profile_background_color_btn.grid(column=1,row=1)
        self.Edit_Verse_profile_background_color_btn.Canvas = self.Edit_server_Verse_profiles_canvas # for mousewheel

        self.Edit_Verse_profile_Text_color_btn = tk.Button(self.Edit_Verse_profile_frame,fg="red",text="Text color",command = lambda x1=server_Verse_profile_Count, x2="fg",x3="Profile":self.Pick_verse_color(x1,x2,x3))
        self.Edit_Verse_profile_Text_color_btn.grid(column=0,row=1)
        self.Edit_Verse_profile_Text_color_btn.Canvas = self.Edit_server_Verse_profiles_canvas # for mousewheel

        self.Edit_Verse_profile_Name_Label = tk.Label(self.Edit_Verse_profile_frame, text="Profile name")
        self.Edit_Verse_profile_Name_Label.grid(column=0,row=0)
        self.Edit_Verse_profile_Name_Label.Canvas = self.Edit_server_Verse_profiles_canvas # for mousewheel

        self.Edit_Verse_profile_Name_entry = tk.Entry(self.Edit_Verse_profile_frame)
        self.Edit_Verse_profile_Name_entry.grid(column=1, row=0)
        self.Edit_Verse_profile_Name_entry.insert(END,Name)
        self.Edit_Verse_profile_Name_entry.Canvas = self.Edit_server_Verse_profiles_canvas # for mousewheel
        server_Verse_profile_Name.append(self.Edit_Verse_profile_Name_entry)

        self.Edit_Verse_profile_Delete_btn = tk.Button(self.Edit_Verse_profile_frame,text="Delete Profile",command = lambda x1=server_Verse_profile_Count:self.Delete_verse_profile(x1))
        self.Edit_Verse_profile_Delete_btn.grid(column=1,row=3)
        self.Edit_Verse_profile_Delete_btn.Canvas = self.Edit_server_Verse_profiles_canvas # for mousewheel
        server_Verse_profile_status.append(True)
        
        server_Verse_profile_Count += 1
        self.Edit_server_Verse_profiles_canvas.configure(scrollregion=self.Edit_server_Verse_profiles_canvas.bbox("all"))

    def add_template_preset(self,Template_list,Name):
        global server_template_preset_Count

        self.Edit_Preset_frame = tk.LabelFrame(self.Edit_server_Template_preset_grid,text="Default Templates by channel")
        self.Edit_Preset_frame.pack()

        self.Edit_Preset_frame.Canvas = self.Edit_server_Template_preset_canvas # for mousewheel

        server_template_preset_Frame.append(self.Edit_Preset_frame)
        self.Edit_Preset_templates_Listbox = tk.Listbox(self.Edit_Preset_frame)
        self.Edit_Preset_templates_Listbox.grid(column=0,row=1,rowspan=4)
        server_template_preset_index.append(self.Edit_Preset_templates_Listbox)
        self.Edit_Preset_templates_Listbox.Canvas = self.Edit_server_Template_preset_canvas # for mousewheel

        self.Edit_Preset_templates_Select_btn = tk.Button(self.Edit_Preset_frame,text="Select_Templates",command = lambda x1="Settings",x2=server_template_preset_Count ,x3="":self.choose_template(x1,x2,x3))
        self.Edit_Preset_templates_Select_btn.grid(column=1,row=2)
        self.Edit_Preset_templates_Select_btn.Canvas = self.Edit_server_Template_preset_canvas # for mousewheel

        self.Edit_Preset_templates_Delete_btn = tk.Button(self.Edit_Preset_frame,text="Delete Preset",command = lambda x1=server_template_preset_Count:self.Delete_template_preset(x1))
        self.Edit_Preset_templates_Delete_btn.grid(column=1,row=3)
        self.Edit_Preset_templates_Delete_btn.Canvas = self.Edit_server_Template_preset_canvas # for mousewheel

        self.Edit_preset_templates_Name_Label = tk.Label(self.Edit_Preset_frame,text="Preset name")
        self.Edit_preset_templates_Name_Label.grid(column=1,row=0)
        self.Edit_preset_templates_Name_Label.Canvas = self.Edit_server_Template_preset_canvas # for mousewheel
        self.Edit_preset_templates_Name_entry = tk.Entry(self.Edit_Preset_frame)
        self.Edit_preset_templates_Name_entry.grid(column=1, row=1)
        self.Edit_preset_templates_Name_entry.insert(END,Name)
        self.Edit_preset_templates_Name_entry.Canvas = self.Edit_server_Template_preset_canvas # for mousewheel

        server_template_preset_Name.append(self.Edit_preset_templates_Name_entry)
        server_template_preset_status.append(True)
        if Template_list == None:
            Template_list = []
            channels = int(settingsXML.get('channels'))
            for x in range(channels):
                Template_list.append("")

        for template in Template_list:
            self.Edit_Preset_templates_Listbox.insert(END,template)
        server_template_preset_Count += 1
        self.Edit_server_Template_preset_canvas.configure(scrollregion=self.Edit_server_Template_preset_canvas.bbox("all"))

    def Delete_template_preset(self,index):
        server_template_preset_Frame[index].destroy()
        server_template_preset_status[index] = False
        self.Edit_server_Template_preset_canvas.configure(scrollregion=self.Edit_server_Template_preset_canvas.bbox("all"))

    def Delete_verse_profile(self,index):
        server_Verse_profile_Frame[index].destroy()
        server_Verse_profile_status[index] = False
        self.Edit_server_Verse_profiles_canvas.configure(scrollregion=self.Edit_server_Verse_profiles_canvas.bbox("all"))

    def Save_server_config(self):
        global settingsXML
        if Connected == True:  # skips saving the server settings if not connected
            channels = int(self.Edit_server_channels.get())
            settingsXML = ET.Element('settings')
            settingsXML.set('channels', self.Edit_server_channels.get())
            settingsXML.set('bible_splitLegnth', self.Edit_server_Bible_splitLegnth.get())
            settingsXML.set('bible_maxlines', self.Edit_server_Bible_Max_lines.get())

            Template = ET.SubElement(settingsXML,'template')
            Verse = ET.SubElement(settingsXML,'verse')
        
        biblename = self.biblename_entry.get()
        if biblename == "":
            biblenameA = "*"
        else:
            biblenameA = biblename
        Server_Ip = self.Ip_address_entry.get()
        Server_port = self.Port_entry.get()

        ClientSettingsXML[0].text = biblenameA
        ClientSettingsXML[1].text = Server_Ip
        ClientSettingsXML[2].text = str(Server_port)

        xmlfile = replace_char(os.getcwd(),'\\','/') + '/client_settings.xml'
        writexml = ET.ElementTree(ClientSettingsXML)
        writexml.write(xmlfile, encoding='unicode')
        if Connected == True: # skips saving the server settings if not connected
            for x in range(0, server_template_preset_Count):
                if server_template_preset_status[x] == True:
                    Preset = ET.SubElement(Template, "preset")
                    Templates_preset = server_template_preset_index[x].get(0)

                    for y in range(1, channels): 
                        Templates_preset = Templates_preset + ',' + server_template_preset_index[x].get(y)
                    Preset.set('name',server_template_preset_Name[x].get())
                    Preset.text = Templates_preset

            for x in range(0, server_Verse_profile_Count):
                if server_Verse_profile_status[x] == True:
                    Profile = ET.SubElement(Verse, "preset")
                    bgcolor = server_Verse_profile_index[x].cget('bg')
                    fgcolor = server_Verse_profile_index[x].cget('fg')
                    colors = fgcolor + ',' + bgcolor
                    Profile.text = colors
                    Profile.set('name',server_Verse_profile_Name[x].get())
                    Preset.text = Templates_preset

            settings = ET.tostring(element=settingsXML, encoding='unicode')
            client.send(DATA_STORE(name="Server_settings", data=str(settings)))
        self.Edit_server_config_frm.destroy()
        print("Settings Saved!")

#################################### end of server config section
#################################### start of select media section

    def choose_media(self, destination, index):
        global LASTFilename
        global Select_media_preview
        global select_media_thumbnail
        
        LASTFilename = ""
        
        try: #removes any open select media windows
            self.select_media_frm.destroy()
        except:
            y=None
        self.select_media_frm = tk.Tk()

        try:
            self.Edit_rundown_item_frame.destroy()
            self.select_media_frm.run_replace = True
        except:
            self.select_media_frm.run_replace = False

        self.select_media_frm.title("Select Media")
        self.select_media_frm.bind('<F1>', clearKeys)
        self.select_media_frm.bind('<F2>', clearKeys)
        self.select_media_frm.bind('<F3>', clearKeys)
        self.select_media_frm.bind('<F4>', clearKeys)
        self.select_media_frm.bind('<F5>', clearKeys)
        self.select_media_frm.bind('<F8>', clearKeys)

        self.select_media_frm.bind('<q>', Media_trim)
        self.select_media_frm.bind('<e>', Media_trim)
        self.select_media_frm.bind('<a>', Media_trim)
        self.select_media_frm.bind('<d>', Media_trim)
        self.select_media_frm.bind('<w>', Media_trim)
        self.select_media_frm.bind('<s>', Media_trim)

        self.display_videos_button = tk.Button(self.select_media_frm, text="Show Videos", command= lambda x1="MOVIE",x2="": self.update_media_listbox(x1,x2)).grid(column=0,row=0)
        self.display_images_button = tk.Button(self.select_media_frm, text="Show Images", command= lambda x1="STILL",x2="": self.update_media_listbox(x1,x2)).grid(column=1,row=0)
        self.display_audio_button = tk.Button(self.select_media_frm, text="Show Audio", command= lambda x1="AUDIO",x2="": self.update_media_listbox(x1,x2)).grid(column=2,row=0)
        self.Preview_Media_button = tk.Button(self.select_media_frm, text="Preview media", command=lambda x1="":self.Preview_selected_media(x1,x1)).grid(column=4,row=0)

        self.loop_media_checkbox = tk.Checkbutton(self.select_media_frm, text="Loop video/Audio")#, onvalue=1, offvalue=0, variable=loop_media, command=self.set_media_looping
        self.loop_media_checkbox.grid(column=0,row=2)
        self.loop_media_checkbox.value = False
        self.loop_media_checkbox.bind('<Return>', checkbox_toggle)
        self.loop_media_checkbox.bind('<Button>', checkbox_toggle)

        self.Fade_media_checkbox = tk.Checkbutton(self.select_media_frm, text="Fade in/fade out from black?")# , onvalue=1, offvalue=0, variable=loop_media,command=self.set_media_looping
        self.Fade_media_checkbox.grid(column=0,row=1)
        self.Fade_media_checkbox.value = False
        self.Fade_media_checkbox.bind('<Return>', checkbox_toggle)
        self.Fade_media_checkbox.bind('<Button>', checkbox_toggle)

        channel_label = tk.Label(self.select_media_frm,text="Caspar channel").grid(column=1,row=1)
        layer_label = tk.Label(self.select_media_frm,text="Video Layer").grid(column=2,row=1)

        self.Media_Channnel_entry = tk.Entry(self.select_media_frm, width = 5)
        self.Media_Channnel_entry.grid(column=1,row=2)

        self.Media_Layer_entry=tk.Entry(self.select_media_frm, width = 5)
        self.Media_Layer_entry.grid(column=2,row=2)

        self.Media_Seek_entry=tk.Entry(self.select_media_frm)
        self.Media_Seek_entry.grid(column=3,row=1)

        self.Media_Legnth_entry=tk.Entry(self.select_media_frm)
        self.Media_Legnth_entry.grid(column=3,row=2)

        self.Media_Title_entry=tk.Entry(self.select_media_frm,width=62)
        self.Media_Title_entry.grid(column=0,row=3,columnspan=3)

        self.Media_Transition_listbox = tk.Listbox(self.select_media_frm, height=1)
        self.Media_Transition_listbox.grid(column=4,row=1)
        transitions = ['CUT','MIX','PUSH','WIPE','SLIDE']
        for transition in transitions:
            self.Media_Transition_listbox.insert(END ,transition)
        self.Media_Transition_listbox.legnth = 4

        self.Media_Duration_entry=tk.Entry(self.select_media_frm)
        self.Media_Duration_entry.grid(column=4,row=2)

        self.Media_Direction_listbox = tk.Listbox(self.select_media_frm,height=1)
        self.Media_Direction_listbox.grid(column=5,row=2)
        Directions = ['LEFT','RIGHT']
        for Direction in Directions:
            self.Media_Direction_listbox.insert(END ,Direction)
        self.Media_Direction_listbox.legnth = 1

        self.Media_Tween_listbox = tk.Listbox(self.select_media_frm,height=1)
        self.Media_Tween_listbox.grid(column=5,row=1)

        self.Media_Tween_listbox.legnth = 42
        Odd = ['Linear','EaseNone']
        a = 'Ease'
        bb = ['In','Out','InOut','OutIn']
        cc = ["Quad",'Cubic','Quart','Quint','Sine','Expo','Circ','Elastic','Back','Bounce']

        for Tween in Odd:
            self.Media_Tween_listbox.insert(END ,Tween)
        for c in cc:
            for b in bb:
                Tween = a+b+c
                self.Media_Tween_listbox.insert(END ,Tween)

        self.add_selected_media = tk.Button(self.select_media_frm, text="Use selected media", command= lambda x1=destination, x2=index: self.add_media_to(x1,x2)).grid(column=3,row=0)
        Seek = "Seek"
        Legnth = "Legnth"
        channel = "1"
        layer = "10"
        looping = False
        fade = False
        duration = "30"
        transition = "MIX"
        direction = "RIGHT"
        tween = "Linear"
        Media_type = None
        title = "Title(enter anything you want)"
        editing = False
        
        if destination == "Slide":
            mediatext = Slide_edit_frame_index[index].media_label.cget("text")
            if mediatext != "No Media":
                medianame = Slide_edit_frame_index[index].media_label.medianame
                title = Slide_edit_frame_index[index].media_label.title

                editing = True
                Media_type = Slide_edit_frame_index[index].media_label.selected_mediatype
                channel = Slide_edit_frame_index[index].media_label.channel
                layer = Slide_edit_frame_index[index].media_label.layer
                looping = Slide_edit_frame_index[index].media_label.looping

                transition = Slide_edit_frame_index[index].media_label.transition
                duration = Slide_edit_frame_index[index].media_label.duration
                direction = Slide_edit_frame_index[index].media_label.direction
                tween = Slide_edit_frame_index[index].media_label.tween
                if Media_type == "MOVIE":                                 
                    fade = Slide_edit_frame_index[index].media_label.fade
                    Seek = Slide_edit_frame_index[index].media_label.seek
                    Legnth = Slide_edit_frame_index[index].media_label.legnth
                    

        elif destination == "rundown":
            if index != -1:
                if RundownItemFrame[index].Type == "Media":
                    editing = True
                    command = RundownItemFrame[index].command
                    medianame = command[0]
                    channel = command[2]
                    Media_type = command[1]
                    layer = command[3]
                    looping = command[4]
                    looping = string_to_bool(looping)
                    transition = command[8]
                    duration = command[9]
                    direction = command[10]
                    tween = command[11]
                    title = command[12]

                    if Media_type == "MOVIE":
                        fade = command[5]
                        fade = string_to_bool(fade)
                        Seek = command[6]
                        Legnth = command[7]
        
        # begin Media_list frame
        self.Media_select_frame = tk.LabelFrame(self.select_media_frm)
        self.Media_select_frame.grid(column=0, row=4, columnspan=4,rowspan=2)

        SC_canvas = add_scrollable_canvas(self.Media_select_frame , "Y", APPapplication, Width=540,G_Width=540)
        self.Media_select_canvas = SC_canvas[0]
        self.Media_select_grid = SC_canvas[1]

        # begin frame contents
        self.Media_filename = tk.Label(self.select_media_frm,text="", bg="green", fg ="white")
        self.Media_filename.grid(column=4, row=3, columnspan=3)

        

        if Media_type != None:
            self.select_media_frm.skip_title = True
            if str(Seek) == "0" and str(Legnth) =="0":
                self.select_media_frm.Skip_disp = True 
                Seek = "Seek"
                Legnth = "Legnth"

                self.update_media_listbox(Media_type, medianame)
            else:
                self.select_media_frm.Skip_disp = False 
                self.select_media_frm.Seek = str(Seek)
                self.select_media_frm.Legnth = str(Legnth)
                self.Media_select_frame.active_name = medianame

                self.update_media_listbox(Media_type, medianame)
          
        else:
            self.select_media_frm.skip_title = False
            self.select_media_frm.Skip_disp = True 
            
            self.Media_filename.configure(text="No file selected !",bg="red" ,fg ="white")
            self.Media_Seek_entry.insert(END, Seek)
            self.Media_Legnth_entry.insert(END, Legnth)
        # print("Seek: " + Seek + " Legnth: " + Legnth)

        self.Media_Channnel_entry.insert(END, channel)
        self.Media_Layer_entry.insert(END, layer)
        self.Media_Duration_entry.insert(END, duration)
        self.Media_Title_entry.insert(END, title)
        
        find_listbox_index(transition ,self.Media_Transition_listbox)
        find_listbox_index(direction ,self.Media_Direction_listbox)
        find_listbox_index(tween ,self.Media_Tween_listbox)
        
        
        if looping == True:
            self.loop_media_checkbox.value = looping
            self.loop_media_checkbox.toggle()

        if fade == True:
            self.Fade_media_checkbox.value = fade
            self.Fade_media_checkbox.toggle()

        if editing == True:
            try:
                self.Media_Layer_entry.delete(0,END)
            except:
                y= None
            try:
                self.Media_Layer_entry.insert(END, layer)
            except:
                y=None
            try:
                get_thumbnail()
            except:
                y=None
    

    def Preview_selected_media(self,Preview_part, overide_legnth):
        global PauseState

        PauseState = True
        time.sleep(.1)
        PauseState = False
        medianame = self.Media_select_frame.active_name
        channels = self.Media_Channnel_entry.get()
        layer = self.Media_Layer_entry.get()
        if Preview_part == "":
            seek = self.Media_Seek_entry.get()
            legnth = self.Media_Legnth_entry.get()
            transition = self.Media_Transition_listbox.get(ACTIVE)
            duration = self.Media_Duration_entry.get()
            direction = self.Media_Direction_listbox.get(ACTIVE)
            tween = self.Media_Tween_listbox.get(ACTIVE)
        else:
            transition = 'CUT'
            duration = 0
            direction = 'RIGHT'
            tween = 'Linear'
            
        # this section is for previewing the start and end of the media trim, depending on the direction either the first 80 frames or the last 80 frames will be played
        seek = self.Media_Seek_entry.get()

        if IsNumber(seek) == False:
            seek = 0
        else:
            seek = int(seek)
            f_seek = seek

        if Preview_part == "Start":
            legnth = str(overide_legnth)
            p_legnth = legnth
            m_seek = seek
            
        elif Preview_part == "End":
            seek = seek + int(self.Media_Legnth_entry.get()) - overide_legnth
            legnth = str(overide_legnth)
            p_legnth = legnth

            m_seek = seek - f_seek
        else:
            m_seek = seek

        m_details = get_media_details(medianame)
        if IsNumber(legnth) == False:
            # legnth = int(media_legnth(medianame, m_details))
            legnth = m_details[3]
            old_legnth = 0
        else:
            legnth = int(legnth)
            old_legnth = legnth

        layer = 5 ############### for pause in print frame function overides default video layer ####################

        Media_channels = channels.split(',')
        client.send(PLAY(video_channel=int(Media_channels[0]), layer=int(layer), clip=medianame, frame=seek, frames=int(legnth), transition=transition, duration=int(duration), direction=direction, tween=tween))
        if m_details[0] == "MOVIE":
            Print_frame(m_seek, p_legnth, m_details)#) self.after(1, 
        
    def add_media_to(self, destination, index):
        global selected_mediatype
        global RundownItemCnt

        Replace = self.select_media_frm.run_replace
        medianame = self.Media_select_frame.active_name
        channel = self.Media_Channnel_entry.get()
        if channel == "":
            channel = "1"
        layer = self.Media_Layer_entry.get()
        seek = self.Media_Seek_entry.get()
        legnth = self.Media_Legnth_entry.get()
        looping = self.loop_media_checkbox.value
        fade = self.Fade_media_checkbox.value
        transition = self.Media_Transition_listbox.get(ACTIVE)
        duration = self.Media_Duration_entry.get()
        direction = self.Media_Direction_listbox.get(ACTIVE)
        tween = self.Media_Tween_listbox.get(ACTIVE)
        title = self.Media_Title_entry.get()
        loopingSTR = bool_to_string(looping)
        fadeSTR = bool_to_string(fade)
        channel = replace_char(channel, ',', '.')
        
        if IsNumber(seek) == False:
            seek = "0"
        if IsNumber(legnth) == False:
            legnth = "0"
        if IsNumber(duration) == False:
            if transition == "CUT":
                duration = "0"
            else:
                duration = "30"

        if destination == "rundown":
            if selected_mediatype == "MOVIE":
                bgcolor = "blue"
                command = [medianame, selected_mediatype, channel, layer, loopingSTR, fadeSTR, seek, legnth, transition, duration, direction, tween, title]
                PhotoName = medianame

            if selected_mediatype == "STILL":
                bgcolor = "red"
                command = [medianame, selected_mediatype, channel, layer, "0", "0", "0", "0", transition, duration, direction, tween, title]
                PhotoName = medianame

            if selected_mediatype == "AUDIO":
                bgcolor = "#c805cb"
                command = [medianame, selected_mediatype, channel, layer, loopingSTR, "0", "0", "0", transition, duration, direction, tween, title]
                PhotoName = ""
            if index == -1:
                Currindex = RundownItemCnt
            else:
                Currindex = index
            
            medianameB = title +'\t\tChannel: ' + channel + ' layer: ' + layer
            self.add_rundown_button(bgcolor, medianameB, Currindex, PhotoName, Replace , "Media", command)  
            
            if index == -1:     
                RundownItemCnt += 1


        if destination == "Slide":            
            mediaitm = title + "\t\t Channel: " + str(channel) + " Layer: " + str(layer)

            Slide_edit_frame_index[index].media_label.configure(text=mediaitm, bg="red")
            Slide_edit_frame_index[index].media_label.medianame = medianame
            Slide_edit_frame_index[index].media_label.selected_mediatype = selected_mediatype
            Slide_edit_frame_index[index].media_label.channel = channel
            Slide_edit_frame_index[index].media_label.layer = int(layer)
            Slide_edit_frame_index[index].media_label.looping = looping
            Slide_edit_frame_index[index].media_label.fade = fade
            Slide_edit_frame_index[index].media_label.seek = int(seek)
            Slide_edit_frame_index[index].media_label.legnth = int(legnth)
            Slide_edit_frame_index[index].media_label.transition = transition
            Slide_edit_frame_index[index].media_label.duration = int(duration)
            Slide_edit_frame_index[index].media_label.direction = direction
            Slide_edit_frame_index[index].media_label.tween = tween
            Slide_edit_frame_index[index].media_label.title = title
            # special handler needed
        client.send(STOP(video_channel=1, layer=5))
        self.select_media_frm.destroy()
        self.Rundown_canvas.configure(scrollregion=self.Rundown_canvas.bbox("all"))

    def Display_media_details(self, filename, index, Media_type, details):
        # Gets details on the selected media filename from caspar. 
        # If the file is a photo or a movie the thumbnail is displayed.
        # If the file is a Movie the trim media bar is displayed. 
        global LASTFilename
        global Media_select_item_last

        ### sets the title the curent filename if a title wasn't specified
        try:
            a_name = self.Media_select_frame.active_name
        except:
            a_name = ""
        if self.select_media_frm.skip_title == False:
            if  a_name != filename:
                title = self.Media_Title_entry.get()
                if title == "Title(enter anything you want)" or title == LASTFilename:
                    self.Media_Title_entry.delete(0, END)
                    self.Media_Title_entry.insert(END, filename)
        self.select_media_frm.skip_title = True

        if filename != LASTFilename:
            LASTFilename = filename
            try:
                self.trim_media_Label_frame.destroy()
                self.trim_media_frame.destroy()
            except:
                v=None

            try:
                self.thumbnail_labelFrame.destroy()
                self.Thumbnail.destroy()
                self.trim_media_Label_frame.destroy()
            except:
                v=None
            
            if Media_type != "AUDIO": # checks to see if a thumbnail should be displayed
                mediadetails = details
                print("details: " + str(details))
                for thumbnail in ThumbnailXML:
                    if thumbnail.get('name') == filename:
                        photo = thumbnail.text
                try:
                    self.Thumbnail = tk.PhotoImage(master=self.select_media_frm, data=photo)
                    self.thumbnail_labelFrame = tk.LabelFrame(self.select_media_frm,text=filename)
                    self.thumbnail_labelFrame.grid(column=4, row=4, columnspan=3)

                    self.thumbnail_label = tk.Label(self.thumbnail_labelFrame, image=self.Thumbnail)
                    self.thumbnail_label.pack()
                except Exception as e:
                    print(e)
                    print("Failed to load Thumbnail")
            if Media_type == "MOVIE":

                framerate = fraction_to_float(mediadetails[5]) 
                seconds = round(media_seconds(filename,0,mediadetails))
                duration = str(datetime.timedelta(seconds=seconds))

                # Start of trim media Bar definitions
                self.trim_media_Label_frame = tk.LabelFrame(self.select_media_frm)
                self.trim_media_Label_frame.grid(column=5,row=5)
                
                self.trim_media_frame = tk.Canvas(self.trim_media_Label_frame,width=400, height=90)
                self.trim_media_frame.pack()
                # center lines
                # self.trim_media_Startline = tk.Label(self.trim_media_Label_frame, bg="black")
                # self.trim_media_Startline.place(x=0, y=30, width=0,height=5)

                self.trim_media_centerline = tk.Label(self.trim_media_Label_frame, bg="black")
                self.trim_media_centerline.place(x=0, y=30, width=400,height=5)
                # self.trim_media_Endline = tk.Label(self.trim_media_Label_frame, bg="black")
                # self.trim_media_Endline.place(x=400, y=30, width=0,height=5)
                # center lines
                frames =  int(mediadetails[4])
                Frames_divisor = int(mediadetails[4]) / 380


                # Start of "Start and end frame" calculations  
                seek = None
                if self.select_media_frm.Skip_disp == False:
                    Seek = int(self.select_media_frm.Seek)
                    startTime_x = Seek / Frames_divisor
                    start = round(int(Seek) / framerate)# the x position for the start handle
                    startTime = str(datetime.timedelta(seconds=start))
                    self.Media_Seek_entry.insert(END, str(Seek))
            
                else:
                    startTime_x = 0
                    startTime = "00:00:00"
                    self.Media_Seek_entry.delete(0, END)
                    self.Media_Seek_entry.insert(END,"Seek")
                    
                Legnth = None

                if self.select_media_frm.Skip_disp == False:
                    Legnth = int(self.select_media_frm.Legnth)
                    Legnth = Legnth + Seek
                    endTime_x = Legnth / Frames_divisor
                    end_t = round(Legnth / framerate) # the x position for the end handle
                    endTime = str(datetime.timedelta(seconds=end_t))
                    self.Media_Legnth_entry.insert(END, str(Legnth))

                else:
                    endTime_x = 380
                    endTime = duration
                    self.Media_Legnth_entry.delete(0, END)
                    self.Media_Legnth_entry.insert(END,"Legnth")

                # End of "Start and end frame" calculations

                self.trim_media_Start_time_label = tk.Label(self.trim_media_frame ,text=startTime)# bg="blue",fg="white"
                self.trim_media_Start_time_label.place(x=0, y=70, width=90,height=25)

                self.trim_media_End_time_label = tk.Label(self.trim_media_frame ,text=endTime)# , bg="blue",fg="white"
                self.trim_media_End_time_label.place(x=300, y=70, width=90,height=25)

                self.trim_media_Start_slider = tk.Label(self.trim_media_frame, bg="red",fg="white",text=">")
                self.trim_media_Start_slider.place(x=startTime_x, y=5, width=20,height=25)
                self.trim_media_Start_slider.index = 0
                self.trim_media_Start_slider.Frames = int(mediadetails[4])
                self.trim_media_Start_slider.framerate = framerate

                self.trim_media_End_slider = tk.Label(self.trim_media_frame, bg="red",fg="white",text="<")
                self.trim_media_End_slider.place(x=endTime_x, y=35, width=20,height=25)
                self.trim_media_End_slider.index = 1
                self.trim_media_End_slider.Frames = int(mediadetails[4])
                self.trim_media_End_slider.framerate = framerate

                Master = [self.trim_media_Start_slider, self.trim_media_End_slider] 

                self.trim_media_Start_slider.Container_index = Master
                self.trim_media_Start_slider.Application = APPapplication
                self.trim_media_End_slider.Container_index = Master
                self.trim_media_End_slider.Application = APPapplication

                self.trim_media_Start_slider.bind('<B1-Motion>',  Media_range_motion)
                self.trim_media_Start_slider.bind('<ButtonRelease-1>', Media_range_end)

                self.trim_media_End_slider.bind('<B1-Motion>',  Media_range_motion)
                self.trim_media_End_slider.bind('<ButtonRelease-1>', Media_range_end)
                # End of trim media Bar definitions

            self.Media_filename.configure(text="Selected file: " + filename, bg="green", fg ="white")

            if Media_type == "AUDIO":
                if Media_select_item_last != -1:
                    Media_select_item_index[Media_select_item_last].configure(bg="#c805cb",fg="white")
                Media_select_item_index[index].configure(bg="white",fg="#c805cb")
                Media_select_item_last = index
            self.Media_select_frame.active_name = filename
        self.select_media_frm.Skip_disp = True


    def update_media_listbox(self, MediaType, Active_name): # This function downloads the current media list from the server and then updates the media listbox in choose media. 
        global selected_mediatype
        global Media_select_item_index
        global Media_select_item_last
        global media_button_Thumbnail_index
                    
        try:    #   destroys the buttons from the previous query
            for item in Media_select_item_index:
                item.destroy()
        except:
            y=None            

        selected_mediatype = MediaType
        Media_select_item_index = []
        Media_select_item_last = -1
        media_button_Thumbnail_index = []

        p = True
        cnt = 0
        while p:    # this section of code asks caspar for the template list. and if it fails it will ask again up to 20 times
            try:
                media_list = client.send(CLS())
                # print("media_list: ", media_list)
            except:
                media_list = None
            if cnt == 20:
                p = False
            if media_list != None:
                p = False
            cnt += 1
        media_name = []
        media_type = []
        media_details = []


        self.Media_Layer_entry.delete(0, END)
        if MediaType == "MOVIE":
            self.Media_Layer_entry.insert(END, "10")
            self.Media_Seek_entry.configure(state="normal")
            self.Media_Legnth_entry.configure(state="normal")

        if MediaType == "AUDIO":
            self.Media_Layer_entry.insert(END, "30")
            self.Media_Seek_entry.configure(state="disabled")
            self.Media_Legnth_entry.configure(state="disabled")
            
        if MediaType == "STILL":
            self.Media_Layer_entry.insert(END, "10")
            self.Media_Seek_entry.configure(state="disabled")
            self.Media_Legnth_entry.configure(state="disabled")

        for line in media_list.data:
            medialine = line.split('"')
            media_name.append(medialine[1])
            mediadetails = medialine[2].split(' ')
            if len(mediadetails) == 8:  # for compatibillity with casparCG 2.3
                mediadetailsB = ['', mediadetails[2], str(mediadetails[4]), str(mediadetails[5]), str(mediadetails[6]), str(mediadetails[7])]
            else:
                mediadetailsB = mediadetails
            media_type.append(mediadetailsB[1]) # changed from index of 1 (caspar2.1 beta2)
            media_details.append(mediadetailsB)
        cnt = 0
        for x in range(len(media_name)):
            active_ind = False
            if media_type[x] == MediaType:
                if Active_name == media_name[x]:
                    active_index = cnt
                    active_ind = True
                    self.Display_media_details(Active_name, active_index, media_type[x], media_details[x])
                if MediaType == "AUDIO":
                    bgcolor = "#c805cb"
                    fgcolor = "white"
                    if active_ind == True:
                        fgcolor = "#c805cb"
                        bgcolor = "white"
                    self.media_item_button = tk.Button(self.Media_select_grid, text=media_name[x], anchor="w", width=89,bg=bgcolor, fg=fgcolor, command=lambda x1=media_name[x],x2=cnt,x3=MediaType, x4=media_details[x]:self.Display_media_details(x1,x2,x3,x4))
                    self.media_item_button.pack(fill="x")
                else:
                    success = self.retreve_thumbnail(media_name[x],"Choose_media")
                    if success == False:
                        self.media_item_button = tk.Button(self.Media_select_grid, text=media_name[x], anchor="w", width=89,fg="white", bg="red", command=lambda x1=media_name[x],x2=cnt,x3=MediaType, x4=media_details[x]:self.Display_media_details(x1,x2,x3,x4)) #  width=60, font=('DejaVu Sans', '13')
                    else:
                        self.media_item_button = tk.Button(self.Media_select_grid, image=media_button_Thumbnail_index[len(media_button_Thumbnail_index) - 1], text=media_name[x], anchor="w", width=89,compound="bottom", command=lambda x1=media_name[x],x2=cnt,x3=MediaType, x4=media_details[x]:self.Display_media_details(x1,x2,x3,x4))# width=,height=240, font=('DejaVu Sans', '13')
                    self.media_item_button.pack(fill="x")
                
                self.media_item_button.Canvas = self.Media_select_canvas # for mousewheel
                self.media_item_button.Active = active_ind
                Media_select_item_index.append(self.media_item_button)


                cnt += 1

##################################### end of choose media Section
##################################### start of song selection section

    def choose_song(self, destination,index):
        self.Choose_Song_frm = tk.Tk()
        try:
            self.Edit_rundown_item_frame.destroy()
            self.Choose_Song_frm.Replace=True
            self.Choose_Song_frm.Currindex = index 
        except:
            self.Choose_Song_frm.Replace=False
            self.Choose_Song_frm.Currindex = RundownItemCnt
        add_song_rundown_button = tk.Button(self.Choose_Song_frm, text="Use selected song", command= lambda x1=destination,x2=index:self.choose_songB(x1,x2)).pack()
        self.Song_list = tk.Listbox(self.Choose_Song_frm, width=100, height=20, selectmode="single")
        self.Song_list.pack()
        self.Get_song_list()

    def Get_song_list(self):
        self.Song_list.delete(0,END)
        songlist = client.send(DATA_LIST(sub_directory='songs'))
        songlist = client.send(DATA_LIST(sub_directory='songs'))
        songlist = client.send(DATA_LIST(sub_directory='songs'))
        songlist = songlist.data

        for item in songlist:
            self.Song_list.insert(END, item)

    def choose_songB(self,destination,index):
        global RundownItemCnt
        songname = self.Song_list.get(ACTIVE)
        self.Choose_Song_frm.destroy()
        if destination == "Open":
            self.Load_song(songname)
        elif destination == "Rundown":
            Replace = self.Choose_Song_frm.Replace
            Currindex = self.Choose_Song_frm.Currindex
            songn = songname
            self.add_rundown_button("green", songname, Currindex,"", Replace, "Song" ,songname)
            self.Rundown_canvas.configure(scrollregion=self.Rundown_canvas.bbox("all"))
            if Replace == True:
                RundownItemCnt += 1
            print("song added to rundown")
#################################### end of song selection section
#################################### start of thumbnail section
    def Process_thumbnail_list(self,ThumbnailList):
        global ThumbnailXML
        ThumbnailXML_loaded = load_thumbnail_xml()
        cnt = 0
        modified = False
        for filename in ThumbnailList:
            filename1 = filename.split('"')

            Mod_Size = filename1[2].split(' ')
            if ThumbnailXML_loaded == True:
                Found = False
                for thumbnail in ThumbnailXML:
                    if thumbnail.get('name') == filename1[1]:
                        if thumbnail.get('modified') == Mod_Size[1] and thumbnail.get('size') == Mod_Size[2]:
                            modified = True
                            Found = True
                        else:
                            ThumbnailXML.remove(thumbnail)
                            Found = False
                if Found == False:
                    modified = True
                    self.add_thumbnail_to_index(filename1[1],Mod_Size)
                    print("added thumbnail: " + filename1[1])
            else:
                modified = True                
                self.add_thumbnail_to_index(filename1[1],Mod_Size)
                print("added thumbnail: " + filename1[1])

        if modified == True:        # jankey code?
            xmlfile = replace_char(os.getcwd(),'\\','/') + '/Thumbnail.xml'# jankey code may only work in Windows?
            writexml = ET.ElementTree(ThumbnailXML)
            writexml.write(xmlfile, encoding='unicode')

    def Update_thumbnail_index(self):
        use_master_media = False
        if use_master_media == True: # disables master media list

            self.Test_frame = tk.Tk()
            self.Test_frame.title("Master Media List")
            
            # begin scrolling frame
            self.Temp_document_frame = tk.LabelFrame(self.Test_frame)
            self.Temp_document_frame.grid(column=0,row=0)

            SC_canvas = add_scrollable_canvas(self.Slide_document_frame , "Y", APPapplication, Height=900,Width=270, G_Width=200, G_Height=100)
            self.Temp_document_canvas = SC_canvas[0]
            self.Temp_document_grid = SC_canvas[1]

        success = True
        while success:
            try:
                ThumbnailList = client.send(THUMBNAIL_LIST()).data
                self.Process_thumbnail_list(ThumbnailList)
                success = False
            except Exception as e:
                print(e)
                print("Media scanner may not be running!")

    def add_thumbnail_to_form(self,filename): # Adds a thumbnail to the "Master Media List" form for testing purposes mostly. 
        for thumbnail in ThumbnailXML:
                    if thumbnail.get('name') == filename:
                        self.New_Thumbnail = tk.PhotoImage(master=self.Temp_document_grid, data=thumbnail.text)
                        ThumbnailsampleIndex.append(self.New_Thumbnail)
                        self.Temp_label = tk.Button(self.Temp_document_grid,text=filename, image=ThumbnailsampleIndex[len(ThumbnailsampleIndex)- 1], compound="bottom",command=lambda x1=filename, x2="MOVIE", x3=1, x4=10, x5=False,x6=0,x7=999999999,x8=False,x9="CUT",x10=0,x11='RIGHT',x12='LINEAR':PlayMediaFile(x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12))
                        self.Temp_label.pack()
                        self.Temp_label.Canvas = self.Temp_document_canvas # for mousewheel



    def add_thumbnail_to_index(self,filename, file_details): # Retreves a thumbnail from The casparcg server and adds it to ThumbnailXML.
        success = False
        # asyncio.new_event_loop().run_until_complete(client.connect("caspar-server.local", 6969))
        # print(filename)
        # photo = client_async.send(THUMBNAIL_RETRIEVE(filename=filename))

        # photo = asyncio.new_event_loop().run_until_complete(client_async.send(THUMBNAIL_RETRIEVE(filename=filename)))
        while success == False:
            try: # query's the thumbnail ten times to guarantee the right thumbnail(otherwise caspar will sometimes return the previous thumbnail),    jankey code, Bug in amcp-pylib or amcp? investigating asyncio solution.
            # photo = asyncio.new_event_loop().run_until_complete(client_async.send(THUMBNAIL_RETRIEVE(filename=filename)))
            # photo = client_async.send(THUMBNAIL_RETRIEVE(filename=filename))
               
                photo = client.send(THUMBNAIL_RETRIEVE(filename=filename))
                photo = client.send(THUMBNAIL_RETRIEVE(filename=filename))
                photo = client.send(THUMBNAIL_RETRIEVE(filename=filename))
                # photo = client.send(THUMBNAIL_RETRIEVE(filename=filename))
                # photo = client.send(THUMBNAIL_RETRIEVE(filename=filename))
                # photo = client.send(THUMBNAIL_RETRIEVE(filename=filename))
                # photo = client.send(THUMBNAIL_RETRIEVE(filename=filename))
                # photo = client.send(THUMBNAIL_RETRIEVE(filename=filename))
                Continue = True
            except:
                Continue = False
            if Continue == True:
                try:  # attempts to load the thumbnail into a photoimage as a test

                    Test = tk.PhotoImage(master=self, data=photo.data_str)
                    GoodPhoto = photo.data_str
                    new_thumbnail = ET.SubElement(ThumbnailXML, 'thumbnail')
                    new_thumbnail.text = GoodPhoto
                    new_thumbnail.set('name',filename)
                    new_thumbnail.set('modified',file_details[1])
                    new_thumbnail.set('size', file_details[2])
                    success = True
                except:
                    sleep(.05)

    def retreve_thumbnail(self, Name, destination):# retreves thumbnail from ThumbnailXML
        GoodPhoto = None

        for thumbnail in ThumbnailXML:
            if thumbnail.get('name') == Name:
                GoodPhoto = thumbnail.text

        if GoodPhoto != None:
            if destination == "Choose_media":
                self.thumbnail_choose = tk.PhotoImage(master=self.select_media_frm, data=GoodPhoto)
                media_button_Thumbnail_index.append(self.thumbnail_choose)

            if destination == "Rundown":      
                self.thumbnail_run = tk.PhotoImage(master=self, data=GoodPhoto)
                RundownThumbnailIndex.append(self.thumbnail_run)
                    
            if destination == "Slide Document":
                Thumbnailv = tk.PhotoImage(master=self.VerseLine_Slide_Frame, data=GoodPhoto)
                self.VerseLine_Slide_Frame
                VerselineThumbnailIndex.append(Thumbnailv)
            return True

        if GoodPhoto == None:
            return False
#################################### End of thumbnail section
#################################### start of rundown section

    def add_rundown_button(self, bgcolor, Name, index, photo, Replace, Type,command): # places Buttons on the "Rundown_Frame"
        global RundownItemRow
        global RundownItemPos_index
        index = int(index)
        if Replace == True:
            RundownItemFrame[index].button.destroy()
        else:  
            NewWidgetFrame = add_widget_frame(RundownItemFrame, RundownItemCnt, RundownItemPos_index, RundownItemRow, "Vertical", self.Rundown_grid, self.Rundown_canvas , 535, 160, 0, "")
            Rundown_Item_Frame = NewWidgetFrame[0]
            RundownItemRow = NewWidgetFrame[1]
            RundownItemPos_index = NewWidgetFrame[2] 

            rundownItemDelete_btn = tk.Button(Rundown_Item_Frame, text="Edit",command=lambda x1=RundownItemCnt:self.edit_rundown_item(x1))
            rundownItemDelete_btn.pack(side="right")
            rundownItemDelete_btn.Canvas = self.Rundown_canvas # for mousewheel
        
        RundownItemFrame[int(index)].bgcolor = bgcolor
        RundownItemFrame[int(index)].Type = Type
        RundownItemFrame[int(index)].command = command

        if photo != "":
            success = self.retreve_thumbnail(photo,"Rundown")
            ItemName = Name
            if success == False:
                Rundown_item = tk.Button(RundownItemFrame[index], text=itemname , fg="white", bg=bgcolor, width=60, font=('DejaVu Sans', '13'), command = lambda x1=index: self.ClickRundownItem(x1))
            else:
                RundownItemFrame[index].configure(text=Name)# [0] + '\n' + Name[1]
                Rundown_item = tk.Button(RundownItemFrame[index],  image=RundownThumbnailIndex[len(RundownThumbnailIndex) - 1], font=('DejaVu Sans', '13'), compound="bottom", command = lambda x1=index: self.ClickRundownItem(x1))# width=,height=240
        else:
            Split_Name = textwrap.wrap(Name[0], 40, break_long_words=False)
            ItemName = Name
        
            Rundown_item = tk.Button(RundownItemFrame[index], text=ItemName, fg="white", bg=bgcolor, width=54, font=('DejaVu Sans', '13'), command = lambda x1=index: self.ClickRundownItem(x1))
        RundownItemFrame[int(index)].Name = ItemName

        Rundown_item.pack(side="left")
        RundownItemFrame[int(index)].button = Rundown_item
        Rundown_item.Canvas = self.Rundown_canvas # for mousewheel


    def edit_rundown_item(self,index):
        try:
            self.Edit_rundown_item_frame.destroy()
        except:
            y= None
        self.Edit_rundown_item_frame = tk.Tk()
        self.Edit_rundown_set_song = tk.Button(self.Edit_rundown_item_frame, text="Choose song", command = lambda x1="Rundown",x2=index: self.choose_song(x1,x2)).pack()
        self.Edit_rundown_set_Media = tk.Button(self.Edit_rundown_item_frame, text="Choose Media", command = lambda x1="rundown", x2=index: self.choose_media(x1,x2)).pack()
        self.Edit_rundown_delete = tk.Button(self.Edit_rundown_item_frame, text="Delete Item", command = lambda x1=index: self.delete_rundown_item(x1)).pack()

    def delete_rundown_item(self,index): #removes the rundown item specified by index
        global RundownItemRow
        widget_frame = delete_widget_frame(RundownItemFrame, index, self.Rundown_grid, self.Rundown_canvas, "y", 160)
        RundownItemRow = widget_frame[0]
        self.Edit_rundown_item_frame.destroy()
        print("Item removed")

    def Clear_rundown(self): # removes all rundown items
        global RunDownXML
        global RundownItemFrame
        global RundownItemRow

        for item in RundownItemFrame:
            item.destroy()
            item.state = False
        RunDownXML = ET.Element('RunDown')
        self.Rundown_canvas.configure(scrollregion=self.Rundown_canvas.bbox("all"))
        RundownItemRow = 0
    def refesh_rundown(self):
        try:
            Clear_rundown()
        except:
            y=None
        Load_Rundown("RUNDOWN")
        print("Rundown Refreshed!")
    
    def Save_rundown(self):# saves the current rundown to the server 
        new_RunDownXML = ET.Element('RunDown')
        cnt = 0
        
        for x in range(0 ,len(RundownItemFrame)): 
            for ItemFrame in RundownItemFrame:
                if ItemFrame.state == True:
                    if ItemFrame.Position_index == x:
                        newitem = ET.SubElement(new_RunDownXML, 'item')
                        newitem.set('id',str(cnt))
                        newitem.set('Type',ItemFrame.Type)
                        newitem.set('bgcolor', ItemFrame.bgcolor)
                        newitem.text = ItemFrame.Name
                        command = ItemFrame.command

                        if ItemFrame.Type == "Song":
                            newitem.set('Songname',command)
                        if ItemFrame.Type == "Media":
                            newitem.set('medianame',str(command[0]))
                            newitem.set('selected_mediatype',str(command[1]))
                            newitem.set('channel', str(command[2]))
                            newitem.set('layer', str(command[3]))
                            newitem.set('looping', str(command[4]))
                            newitem.set('fade', str(command[5]))
                            newitem.set('seek', str(command[6]))
                            newitem.set('legnth', str(command[7]))
                            newitem.set('transition', str(command[8]))
                            newitem.set('duration', str(command[9]))
                            newitem.set('direction', str(command[10]))
                            newitem.set('tween', str(command[11]))
                            newitem.set('Title', command[12])
                        cnt += 1

        rundown = ET.tostring(element=new_RunDownXML, encoding='unicode')#      converts RundownXML to a string
        client.send(DATA_STORE(name=Rundown_name, data=rundown))#       saves the Rundown on the caspar Server
        self.Clear_rundown()
        Load_Rundown("RUNDOWN")
        print("Rundown saved!")

    def ClickRundownItem(self,index): # translates the rundown item index number to the appropriate command
        for item in RundownItemFrame:
            if item.index == int(index):
                UseRundownItem(item.Position_index)

##########################################    End of Rundown section
##########################################    Start of song section

    def Load_song(self, load_song_name): # Loads a song and displays all the slides for use. 
        global songxml
        global versetemplate
        global versecnt
        # global songname
        global VerseText
        global VerseLineBtnCnt
        global VerseLineBtnIndex
        global VerseLineBtnIndexLast
        global VerselineButton
        global last_BG
        global LastTemplate
        global VerseHotkey
        global VerseHotkeyIndex
        global VerseLineSlideFrame
        global VerselineThumbnailIndex

        last_BG = "First"

        songname = load_song_name
        self.songname = load_song_name
        textsize = 13

        success = False
        CNTb = 0
        
        while success == False: # retreves the song data from the server
            try:
                song = client.send(DATA_RETRIEVE(name=songname)).data_str
                song = client.send(DATA_RETRIEVE(name=songname)).data_str
                success = True
            except:
                print("Fail: " + str(CNTb))
                CNTb += 1
        songxml = ET.fromstring(song)

            
        versecnt = 0
# # # # # # # # # # #    Gets a verse count    # # # # # # # # # # # # #
        for child in songxml[0]:
            versecnt += 1

        verseline_cnt = [0 for x in range(versecnt)] 

# # # # # # # # # # # # # #    creates current playlist    # # # # # # # # # # # # # # 

        try:
            self.Slide_document_frame.destroy()
        except:
            y=None

        # begin scrolling frame
        self.Slide_document_frame = tk.LabelFrame(self, text=songname)
        self.Slide_document_frame.grid(column=1,row=1,sticky="ns")#codechange11

        SC_canvas = add_scrollable_canvas(self.Slide_document_frame , "Y", APPapplication, Height=900,Width=1300) # Height=900,Width=1300#codechange11
        self.Slide_document_canvas = SC_canvas[0]
        self.Slide_document_grid = SC_canvas[1]

        # begin frame contents
       
# # # # # # # # # # # # # #    process the template    # # # # # # # # # # # # # # #

        versetemplate = songxml.find('template').text
        LastTemplate = versetemplate.split(',')

# # # # # # # # # # # # # #    Parses the arangement    # # # # # # # # # # # # # # 
        arangement = songxml.find('arangement').text
        if arangement != None:
            try:
                arangement = arangement.split(',')
            except:
                arangement = [arangement,"x"]

            row = 0
            col = 0
            VerseText = []
            VerseLineBtnCnt = 0
            VerseLineBtnIndex = -1
            VerselineButton = []
            VerseLineSlideFrame = []
            VerselineThumbnailIndex = []
            VerselineThumbnailCnt = 0
            VerseLineBtnIndexLast = 0
            VerseHotkey = []
            VerseHotkeyIndex = []
            
            for Verseid in arangement:
                load = False
                for index in songxml:
                    if index.tag == "verse":
                        for verseN in index:
                            if verseN.get("id") == Verseid:
                                versename = verseN.get("name")
                                hotkey = verseN.get("hotkey")
                                Verse = verseN
                                load = True
                                for option in verseN:
                                    if option.tag == "FGcolor":
                                        fgcolor = option.text
                                    if option.tag == "BGcolor":
                                        bgcolor = option.text
                if load == True:
                    try:
                        if hotkey != "":
                            versename = versename + " Hotkey: " + hotkey
                            VerseHotkeyIndex.append(VerseLineBtnCnt)
                            VerseHotkey.append(hotkey)
                    except:
                        y=None

                    self.verselabel = tk.Label(self.Slide_document_grid, text=versename, font=('DejaVu Sans', textsize))
                    self.verselabel.grid(column=col, row=row)
                    self.verselabel.Canvas = self.Slide_document_canvas # for mousewheel

                    for Slide in Verse:
                        if Slide.tag == "slide":
                            Slideid = Slide.get("id")
                            MediaName = Slide.get("MediaName")
                            slideText = Slide.text
                            frametext = ""
                            if MediaName != "":    
                                    title = Slide.get("MediaTitle")
                                    MediaTextA = "Name: " +  title
                                    MediaTextB = "Type : " + Slide.get("mediaType") + "  Channel: " + Slide.get('channel') + "  Layer: " + Slide.get('layer')
                                    
                            if slideText == "\t":# if slide is blank
                                if MediaName == "": # if there is no media
                                    verseline = "`Blank Slide`"
                                else:
                                    verseline = MediaTextA + "\n" + MediaTextB

                            else: # the slide is not blank
                                if MediaName != "": # there is media
                                    verseline = slideText
                                    frametext = MediaTextA + "\t" + MediaTextB
                                else:# there is no media
                                    verseline = slideText

                            VerseText.append(Verseid + "," + Slideid)
                
                            self.VerseLine_Slide_Frame = tk.LabelFrame(self.Slide_document_grid, text=frametext, )#width=600, height=600 bg="red"
                            self.VerseLine_Slide_Frame.grid(column=col, row=row +1,padx=5,pady=5)
                            self.VerseLine_Slide_Frame.Canvas = self.Slide_document_canvas # for mousewheel
                            # Grid.rowconfigure(self.VerseLine_Slide_Frame, 0, weight=1)
                            # Grid.columnconfigure(self.VerseLine_Slide_Frame, 0, weight=1)

                            if MediaName != "":
                                media_details = get_media_details(MediaName)
                                success = False
                                # print("media_details[1]: " + media_details[1])
                                if media_details[0] == "MOVIE" or media_details[0] == "STILL":
                                    success = False
                                    while success == False:
                                        # print("MediaName: " + MediaName)
                                        success = self.retreve_thumbnail(MediaName,"Slide Document")
                                    self.verseline_button = tk.Button(self.VerseLine_Slide_Frame, image=VerselineThumbnailIndex[VerselineThumbnailCnt], text=verseline, fg=fgcolor, bg=bgcolor, compound="bottom", width=390, height=210, highlightthickness=4, font=('DejaVu Sans', textsize), command = lambda x1=VerseLineBtnCnt: self.send_lyric(x1))
                                    VerselineThumbnailCnt += 1

                                else:
                                  self.verseline_button = tk.Button(self.VerseLine_Slide_Frame, text=verseline, fg=fgcolor, bg=bgcolor, width=44, height=10, highlightthickness=4, font=('DejaVu Sans', textsize), command = lambda x1=VerseLineBtnCnt: self.send_lyric(x1))  
                            else:
                                self.verseline_button = tk.Button(self.VerseLine_Slide_Frame, text=verseline, fg=fgcolor, bg=bgcolor, width=44, height=10, highlightthickness=4, font=('DejaVu Sans', textsize), command = lambda x1=VerseLineBtnCnt: self.send_lyric(x1))
                            self.verseline_button.grid(column=0,row=0)#fill="both", expand="yes"
                            VerselineButton.append(self.verseline_button)

                            self.verseline_button.Canvas = self.Slide_document_canvas# for mousewheel
                            
                            VerseLineSlideFrame.append(self.VerseLine_Slide_Frame)###########
                            VerseLineBtnCnt += 1
                            col += 1
                            if col >= 3: # determins the number of columns to display
                                col = 0
                                row += 2
        else:
            print("Song has no arangement!") 
        self.EditSong(songname)
        print("Song loaded!")
        

    def EditSong(self, songnam):
        # global songxml
        global versecnt
        global songname
        global arangement
        global versetemplate
        

        versecnt = 0
# ## # # # # # # # get arangement
        for child in songxml:
            if child.tag == "arangement":
                arangement = child.text
                if arangement != None:
                    arangement = arangement.split(',')

# # # # # # # # # # #    Gets a verse count    # # # # # # # # # # # # #
        for child in songxml[0]:
            versecnt += 1

        for child in songxml:
            if child.tag == "template":
                template = child.text

        # begin scrolling frame
        self.Verse_Select_frame = tk.LabelFrame(self.editverse) # text=songname
        self.Verse_Select_frame.grid(column=0,row=1,columnspan=9)

        SC_canvas = add_scrollable_canvas(self.Verse_Select_frame , "Y", APPapplication, Height=30, Width=800, G_Width=200, G_Height=100)
        self.Verse_Select_canvas = SC_canvas[0]
        self.Verse_Select_grid = SC_canvas[1]


# # # # # # # # # # # # # #    Gets the default template    # # # # # # # # # # # # # # 
        versetemplate = songxml.find('template').text

# # # # # # # # # # # # # #    Creates verse list          # # # # # # # # # # # # # # 
        count = 0#begin jankey code
        for child in songxml[0]:
            versename = child.get("name")
            VerseID = child.get("id")
            for subchild in child:
                if subchild.tag == "BGcolor":
                    bgcolor = subchild.text
                if subchild.tag == "FGcolor":
                    fgcolor = subchild.text    
                   
            try:
                self.versebtn = tk.Button(self.Verse_Select_grid, text=versename, fg=fgcolor, bg=bgcolor, font=('DejaVu Sans', '12'), command = lambda x1=VerseID,x2=fgcolor,x3=bgcolor: self.new_verse(x1,x2,x3))
            except:
                self.versebtn = tk.Button(self.Verse_Select_grid, text=versename, fg="white", bg="blue", font=('DejaVu Sans', '12'), command = lambda x1=VerseID,x2=fgcolor,x3=bgcolor: self.new_verse(x1,x2,x3))
            self.versebtn.grid(column=count,row=0)
            count += 1
        # end jankey code
        print("Song loaded for editing!")   

    def new_verse(self, verseID, FGcolor, BGcolor):
        global Slide_edit_frame_index

        global new_fgcolor
        global new_bgcolor
        new_fgcolor = FGcolor
        new_bgcolor = BGcolor
        global NewSlide_Row
        global NewSlideCnt
        global NewSlide_pos_index

        Slide_edit_frame_index = []
        NewSlide_Row = 0
        NewSlideCnt = 0
        NewSlide_pos_index = 0

        if verseID == "N":
            verseID = versecnt

        for child in songxml:
            if child.tag == "template":
                    template = child.text     
        default_template = template.split(',')

        try:    # removes any open editverse windows
            self.NewVerseFrm.destroy()
        except:
            y=None
        
        self.NewVerseFrm = tk.Tk()
       
        self.NewVerseFrm.bind('<F1>', clearKeys)
        self.NewVerseFrm.bind('<F2>', clearKeys)
        self.NewVerseFrm.bind('<F3>', clearKeys)
        self.NewVerseFrm.bind('<F4>', clearKeys)
        self.NewVerseFrm.bind('<F5>', clearKeys)
        self.NewVerseFrm.bind('<F6>', clearKeys)
        self.NewVerseFrm.bind('<F7>', clearKeys)
        self.NewVerseFrm.bind('<F8>', clearKeys)
        self.NewVerseFrm.bind("<Control-r>", APPapplication.Split_slide_text)
        self.NewVerseFrm.bind("<Control-d>", APPapplication.Condense_slide_Text)
        
        label = tk.Label(self.NewVerseFrm, text="New verse name").grid(column=0,row =0)
        self.new_verse_name = tk.Entry(self.NewVerseFrm)
        self.new_verse_name.grid(column=0, row=1)
        self.AddVerseButton = tk.Button(self.NewVerseFrm, text="Save Verse", command=lambda x1=verseID, x2="slide_edit": self.SaveVerse(x1,x2)).grid(column=5, row=1)
        self.AddVerseButton = tk.Button(self.NewVerseFrm, text="Delete Verse", command=lambda x1=verseID: self.Delete_verse(x1)).grid(column=5, row=0)
        
        self.foreground_color_button = tk.Button(self.NewVerseFrm,text="Text Color", fg="red", command=lambda x1="",x2="fg",x3="Slides":self.Pick_verse_color(x1,x2,x3))
        self.foreground_color_button.grid(column=1, row=0)

        self.background_color_button = tk.Button(self.NewVerseFrm,text="Background Color", bg="red", command=lambda x1="",x2="bg",x3="Slides":self.Pick_verse_color(x1,x2,x3))
        self.background_color_button.grid(column=2, row=0)

        self.sample_button = tk.Label(self.NewVerseFrm, text="Sample", fg="white",bg="black")
        self.sample_button.grid(column=2, row=1)
        self.Add_new_slide = tk.Button(self.NewVerseFrm,text="Add slide", command= lambda x1="",x2="",x3=default_template,x4=default_template,x5="",x6="",x7="",x8=False:self.Add_slide(x1,x2,x3,x4,x5,x6,x7,x8))
        self.Add_new_slide.grid(column=1,row=1)
        self.cancel_Verse_changes = tk.Button(self.NewVerseFrm, text="Cancel changes",command=self.NewVerseFrm.destroy).grid(column=6,row=1)

        self.verse_profiles_listbox = tk.Listbox(self.NewVerseFrm,height=3)
        self.verse_profiles_listbox.grid(column=4,row=0,rowspan=2)
        self.verse_profiles_listbox.bind('<Return>',use_Verse_profile)

        for VerseProfile in settingsXML:
            if VerseProfile.tag == "verse":
                for profile in VerseProfile:
                     self.verse_profiles_listbox.insert(END,profile.get('name'))

        self.Verse_hotkey_label = tk.Label(self.NewVerseFrm, text="Verse Hotkey: ").grid(column=3,row=0)
        self.Verse_hotkey_Entry = tk.Entry(self.NewVerseFrm)
        self.Verse_hotkey_Entry.grid(column=3,row=1)

        # begin scrolling frame
        self.Verseedit_frame = tk.LabelFrame(self.NewVerseFrm)
        self.Verseedit_frame.grid(column=0,row=2,columnspan=7,)

        SC_canvas = add_scrollable_canvas(self.Verseedit_frame , "Y", APPapplication, Height=900, Width=1200, G_Width=1200, G_Height=0)
        self.Verseedit_canvas = SC_canvas[0]
        self.verse_entry_grid = SC_canvas[1]

        # begin frame contents
        versename = ""
        skip = False
        for verse_element in songxml:
            for verse in verse_element:
                if verse.get("id") == verseID:
                    skip = True
                    versename = verse.get("name")
                    hotkey = verse.get("hotkey")
                    try:
                        if hotkey != "":
                            self.Verse_hotkey_Entry.insert(END,hotkey)
                    except:
                        y=None
                    self.NewVerseFrm.title(versename)
                    self.new_verse_name.insert(END,versename)
                    for slide in verse:
                        if slide.tag == "slide":
                            slide_text = slide.text
                            medianame = slide.get("MediaName")
                            slide_REF = slide.get("REF")
                            if slide_REF == None:
                                slide_REF = ""
                            header = slide.get("Header")
                            if header == '\t':
                                header = ""
                            try:
                                slide_Header = replace_char(header, '[---]', '\n')
                            except:
                                slide_Header = header  
                            if slide_Header == None:
                                slide_Header = ""
                            Slide_timer = slide.get("timer")
                            slide_template = slide.get("template")
                            slide_template = slide_template.split(',')

                            if medianame != "":
                                mediaType = slide.get("mediaType")
                                channel = slide.get("channel")
                                layer = slide.get("layer")
                                loop = slide.get("looping")
                                fade = slide.get("fade")
                                seek = slide.get("seek")
                                legnth = slide.get("legnth")
                                transition = slide.get("transition")
                                duration = slide.get("duration")
                                direction = slide.get("direction")
                                tween = slide.get("tween")
                                title = slide.get("MediaTitle")
                                if title == None:
                                    title = medianame

                                slide_media ='Name: ' + medianame + ' Type: ' + mediaType + " Channel: " + channel + ' Layer: ' + layer + ' Looping: ' + str(loop) + ' Fade: ' + str(fade) + ' Seek: ' + seek + ' Legnth: ' + legnth + ' Transition: ' + transition + ' Duration: ' + duration + ' Direction: ' + direction + ' Tween: ' + tween
                                mediadata = [medianame, mediaType, channel, int(layer), string_to_bool(loop), string_to_bool(fade), int(seek), int(legnth), transition, int(duration), direction, tween, title]
                            else:
                                slide_media = "" 
                                mediadata = False
                            if slide_text == "\t":
                                slide_text = ""
                            self.Add_slide(slide_text, slide_media, slide_template, default_template, slide_REF, slide_Header,Slide_timer, mediadata)
        if skip == False:
            self.Add_slide("", "", default_template, default_template,"","","", False)
        self.NewVerseFrm.title("Editing: " + versename)
        
    def delete_slide(self, index):
        global NewSlide_Row
        widget_frame = delete_widget_frame(Slide_edit_frame_index, index, self.verse_entry_grid, self.Verseedit_canvas, "y", 160)
        NewSlide_Row = widget_frame[0]

    def Preview_slide(self, index):
        global LastTemplate
        global fade_channels
        global fade_layer
        global fade_seconds

        channels = int(settingsXML.get('channels'))
        media = Slide_edit_frame_index[index].media_label.cget('text')
        REF = Slide_edit_frame_index[index].Reference_entry.get()
        header = Slide_edit_frame_index[index].Header_entry.get(1.0,END)
        Verse = Slide_edit_frame_index[index].entry.get(1.0,END)

        try:
            verseb = Slide_entry_Index[index + 1].get(1.0,END)
        except:
            verseb = ""
        template_list = []

        for x in range(0,channels):
            try:
                template_list.append(Slide_edit_frame_index[index].Template_label.get(x))
            except:
                template_list.append("")
        
        if media != "No Media":
            medianame = Slide_edit_frame_index[index].media_label.medianame
            selected_mediatype = Slide_edit_frame_index[index].media_label.selected_mediatype
            Media_channels = Slide_edit_frame_index[index].media_label.channel
            layer = Slide_edit_frame_index[index].media_label.layer
            loop = Slide_edit_frame_index[index].media_label.looping
            fade = Slide_edit_frame_index[index].media_label.fade
            seek = Slide_edit_frame_index[index].media_label.seek
            # print("important: ",Slide_edit_frame_index[index].media_label.legnth)
            legnth = Slide_edit_frame_index[index].media_label.legnth
            transition = Slide_edit_frame_index[index].media_label.transition
            duration = Slide_edit_frame_index[index].media_label.duration
            direction = Slide_edit_frame_index[index].media_label.direction 
            tween = Slide_edit_frame_index[index].media_label.tween
            Media_channels = Media_channels.split(',')
            for channel in Media_channels:
                PlayMediaFile(medianame, selected_mediatype, int(channel), layer, loop, seek, legnth, fade, transition, duration, direction, tween)

        try:
            nonetype = LastTemplate
        except:
            LastTemplate = []
            for x in range(0, channels):
                LastTemplate.append("")

        for x in range(len(LastTemplate)):
            if template_list[x] != LastTemplate[x]: 
                update_template = True
                clear_channel(x + 1, 20,1)
                LastTemplate[x] = template_list[x] 

        verse_list = Verse.split('\n')
        verse = []
        verseId = []
        for x in range(0,5):
            try:
                verse.append(verse_list[x])
            except:
                verse.append("")
            verseId.append("f" + str(x))

        if verse[0] == "": # was \t
            for x in range(1, channels + 1):
                clear_channel(x, 20,1)
        else:
            if header != '\n':
                header = header.split('\n')
                for x in range(len(header)):
                    verse.append(header[x])
                    verseId.append('h' + str(x))
            if REF != "":
                verse.append(REF)
                verseId.append("ref")
        
            if verseb != "":
                verseb = verseb.split('\n')
                for x in range(0,5):
                    try:
                        verse.append(verseb[x])
                    except:
                        verse.append("")
                    verseId.append("b" + str(x))
            use_template(20, 1, template_list, verse, verseId)

    def split_text_to_versesA(self):
        self.split_verses_Frm = tk.Tk()
        self.Slide_entry = Text(self.slide_edit_frame,width=45, height=5, pady=10)
        self.Slide_entry.grid(column=0,row=2,columnspan=4, rowspan=5)
        self.Slide_entry.insert(1.0, slide_text)
        self.slide_edit_frame.entry = self.Slide_entry

    def Split_slide_text(self,event): # splits the text in the current slide baised on \n\n, into multiple slides.
        global NewSlide_Row
        NewSlide_row = 0
        channels = int(settingsXML.get('channels'))
        for item in songxml:
            if item.tag == "template":
                template = item.text
        template = template.split(',')

        newText = Slide_edit_frame_index[NewSlideCnt - 1].entry.get(1.0,END)
        newText = newText[:-1]
        first_media = Slide_edit_frame_index[NewSlideCnt - 1].media_label.cget('text')
        if first_media == "No Media":
            first_media = ""
        first_template = []
        for x in range(0,channels):
            first_template.append(Slide_edit_frame_index[NewSlideCnt -1].Template_label.get(x))

        self.delete_slide(NewSlideCnt - 1)
        try:
            newText = newText.split('\n\n')
            first = True
            for text in newText:
                if first == True:
                    self.Add_slide(text, first_media, first_template, template,"","","",False)
                    first = False
                else:
                    self.Add_slide(text, "", template, template,"","","",False)
        except:
            print("Could not split text! Please hit Enter twice to indicate where to split.\nlikethis:\nLine1.\nline2.\n\nline3\nline4")

    def Condense_slide_Text(self,event): # condenses all slides in the current verse into one slide(all customizations are lost!)
        for item in songxml:
            if item.tag == "template":
                template = item.text 
        template = template.split(',')

        for x in range(0, NewSlideCnt):
            if Slide_edit_frame_index[x].state == True:
                if x == 0:
                    text = Slide_edit_frame_index[x].entry.get(1.0,END)
                    self.delete_slide(x)
                else:
                    text = text + '\n' + Slide_edit_frame_index[x].entry.get(1.0,END)
                    self.delete_slide(x)
        self.Add_slide(text, condensed_media[0], template, template,"","","",False)

    def clear_slide_media(self,index):
        global Slide_edit_frame_index
        Slide_edit_frame_index[index].media_label.configure(text="No Media",bg="green")
        # x1=NewSlideCnt:Slide_media_label_Index[x1].configure

    def Add_slide(self,slide_text, Media, Template, default_template,ref,header,timer, mediadata): # adds a slide to the verse edit form
        global NewSlide_Row
        global NewSlideCnt
        global NewSlide_pos_index

        if Media == "":
            medianame = "No Media"
            BG_color = "green"
        else:
            medianame = Media
            BG_color = "red"

        if Template == default_template:
            template_BG = "green"
        else:
            template_BG = "red"
        channels = int(settingsXML.get('channels'))
        
        # begin widget sorting connector
        NewWidgetFrame = add_widget_frame(Slide_edit_frame_index, NewSlideCnt, NewSlide_pos_index, NewSlide_Row, "Vertical", self.verse_entry_grid, self.Verseedit_canvas , 1200, 160, 0, "")
        slide_edit_frame = NewWidgetFrame[0]
        NewSlide_Row = NewWidgetFrame[1]
        NewSlide_pos_index = NewWidgetFrame[2] 
        
        # begin frame contents
        Slide_entry_label = tk.Label(slide_edit_frame, text="Slide Text, displayed as f0 to \"Bible, max lines per slide\"(see settings)").grid(column=0,row=1,columnspan=4)

       
        Slide_entry = Text(slide_edit_frame,width=45, height=5, pady=10)
        Slide_entry.grid(column=0,row=2,columnspan=4, rowspan=5)# pack()
        Slide_entry.insert(1.0, slide_text)
        slide_edit_frame.entry = Slide_entry

        Delete_slide_btn = tk.Button(slide_edit_frame, text="Delete slide", command= lambda x1=NewSlideCnt:self.delete_slide(x1))#.grid(column=4, row=NewSlide_Row + 3, padx=10)
        Delete_slide_btn.grid(column=4, row=3, padx=10)
        Delete_slide_btn.Canvas = self.Verseedit_canvas # for mousewheel

        Slide_Play_Btn = tk.Button(slide_edit_frame, text="Play Slide", command= lambda x1=NewSlideCnt:self.Preview_slide(x1))#.grid(column=4, row=NewSlide_Row + 2,padx=10)
        Slide_Play_Btn.grid(column=4, row=2,padx=10)
        Slide_Play_Btn.Canvas = self.Verseedit_canvas # for mousewheel

        Slide_media_label = tk.Label(slide_edit_frame, text=medianame, fg="white",bg=BG_color)
        Slide_media_label.grid(column=0, row=0, columnspan=10)
        Slide_media_label.Canvas = self.Verseedit_canvas # for mousewheel
        slide_edit_frame.media_label = Slide_media_label

        if mediadata != False:
            Slide_media_label.medianame = mediadata[0]
            Slide_media_label.selected_mediatype = mediadata[1]
            Slide_media_label.channel = mediadata[2]
            Slide_media_label.layer = mediadata[3]
            Slide_media_label.looping = mediadata[4]
            Slide_media_label.fade = mediadata[5]
            Slide_media_label.seek = mediadata[6]
            Slide_media_label.legnth = mediadata[7]
            Slide_media_label.transition = mediadata[8]
            Slide_media_label.duration = mediadata[9]
            Slide_media_label.direction = mediadata[10]
            Slide_media_label.tween = mediadata[11]
            Slide_media_label.title = mediadata[12]
            labeltext = mediadata[12] + "\t\t Channel: " + str(mediadata[2]) + " Layer: " + str(mediadata[3])
            Slide_media_label.configure(text=labeltext)


        Slide_media_Btn = tk.Button(slide_edit_frame, text="Edit Media", command= lambda x1="Slide",x2=NewSlideCnt:self.choose_media(x1,x2))
        Slide_media_Btn.grid(column=5, row=3)
        Slide_media_Btn.Canvas = self.Verseedit_canvas # for mousewheel

        Slide_remove_media_button = tk.Button(slide_edit_frame, text="Remove Media", command= lambda x1=NewSlideCnt:self.clear_slide_media(x1))
        Slide_remove_media_button.grid(column=5, row=2)
        Slide_remove_media_button.Canvas = self.Verseedit_canvas # for mousewheel

        Slide_Template_label = tk.Listbox(slide_edit_frame,bg=template_BG, fg="white", height=4, width= 25)
        Slide_Template_label.grid(column=6, row=2)
        Slide_Template_label.Canvas = self.Verseedit_canvas # for mousewheel
        slide_edit_frame.Template_label = Slide_Template_label

        xcnt = 0
        template_list = []

        if len(Template) <= channels:
            for x in range(len(Template) ,channels):
                Template.append("")
            for item in Template:
                template_list.append(item)
        else:
            for x in range(0,channels -1):
                template_list.append(Template[x])

        for item in template_list:
            Slide_Template_label.insert(xcnt,item)
            xcnt += 1

        Slide_Template_Btn = tk.Button(slide_edit_frame, text="Change template", command= lambda x1="Slide",x2=NewSlideCnt,x3=default_template:self.choose_template(x1,x2,x3))
        Slide_Template_Btn.grid(column=6, row=3, sticky=N)
        Slide_Template_Btn.Canvas = self.Verseedit_canvas # for mousewheel

        Header_entry_label = tk.Label(slide_edit_frame, text="Slide Header, displayed as h0 to whatever").grid(column=8 ,row=1)
        Header_entry = Text(slide_edit_frame,width=30, height=2)
        Header_entry.grid(column=8,row=2)
        Header_entry.insert(END,header)
        slide_edit_frame.Header_entry = Header_entry
        
        Reference_entry_label = tk.Label(slide_edit_frame, text="Slide reference, displayed as \"ref\"").grid(column=8 ,row=3)
        Reference_entry = tk.Entry(slide_edit_frame)
        Reference_entry.grid(column=8 ,row=4)
        Reference_entry.insert(END,ref)
        slide_edit_frame.Reference_entry = Reference_entry

        Slide_Timer_Label = tk.Label(slide_edit_frame,text="Go to next slide timer")#.grid(column=9 ,row=NewSlide_Row + 2)
        Slide_Timer_Label.grid(column=9 ,row=2)
        Slide_Timer_Label.Canvas = self.Verseedit_canvas # for mousewheel

        Slide_Timer_entry = tk.Entry(slide_edit_frame)
        Slide_Timer_entry.grid(column=9 ,row=3)
        Slide_Timer_entry.insert(END,timer)
        slide_edit_frame.Timer_entry = Slide_Timer_entry

        NewSlideCnt += 1

    def SaveVerse(self,VerseID, source):#jankey function saves verse data to "Songxml"
        global songxml
        if source == "slide_edit":
            Versename = self.new_verse_name.get()
        if source == "Bible":
            if self.loadverse_frm.singlechapter == True:
                Versename = self.loadverse_frm.book + ' ' +  str(self.loadverse_frm.startchapter) + ':' + str(self.loadverse_frm.startverse)
            else:
                Versename = self.loadverse_frm.book + ' ' +  str(self.loadverse_frm.startchapter) + ':' + str(self.loadverse_frm.startverse) + " - " + str(self.loadverse_frm.book) + " " + str(self.loadverse_frm.endchapter) + ":" + str(self.loadverse_frm.endverse)

        newverse = True
        VerseID = str(VerseID)
        channels = int(settingsXML.get('channels'))
        
        for item in songxml:    #retreves the right verse element from songxml
            if item.tag == "verse":
                vpatent= item
                for verseELE in item:
                    if verseELE.tag == "verse":
                        if verseELE.get("id") == VerseID:
                            newverse = False
                            Verse = verseELE
                            item.remove(verseELE)
                            Verse = ET.SubElement(item, "verse")

        if newverse == True:    # adds a new element to songxml if the current verse is not found
            for item in songxml:
                if item.tag == "verse":
                    Verse = ET.SubElement(item, "verse")

            for item in songxml: # If the verse is new, it is automatically added to the current arangement
                if item.tag == "arangement":
                    if item.text == None:
                        item.text = VerseID
                    else:
                        item.text = item.text + ',' + VerseID

        Verse.set("name", Versename)
        Verse.set("id", VerseID)        
        if source == "slide_edit":
            Verse.set("hotkey",self.Verse_hotkey_Entry.get())
        count = 0
        if source == "slide_edit":
            
            for x in range(len(Slide_edit_frame_index)):
                for ItemFrame in Slide_edit_frame_index:
                    if ItemFrame.state == True:
                        if ItemFrame.Position_index == x:
                            medianame = ItemFrame.media_label.cget("text")

                            slide = ET.SubElement(Verse, 'slide')
                            SlideText = ItemFrame.entry.get(1.0, END)
                            SlideText = SlideText[:-1]

                            if SlideText == "":
                                SlideText = "\t"  
                            slide.text = SlideText
                            slide.set("id", str(count))
                            for x1 in range(0,channels):
                                if x1 == 0:
                                    template_list = ItemFrame.Template_label.get(x1)
                                else:
                                    try:
                                        template_list = template_list + ',' + ItemFrame.Template_label.get(x1)
                                    except:
                                        template_list = template_list + ',' + ""

                            slide.set("template", template_list)#Slide_Template_label_index[x].cget("text")
                            header = ItemFrame.Header_entry.get(1.0,END)
                            header = header[:-1]
                            if header == "":
                                header = "\t"
                            try:
                                slide_header = header = replace_char(header, '\n', '[---]')
                            except:
                                slide_header = header

                            slide.set("timer", ItemFrame.Timer_entry.get())
                            slide.set("REF", ItemFrame.Reference_entry.get())
                            slide.set("Header", slide_header)

                            if medianame != "No Media":
                                # media = media.split(",")
                                slide.set("MediaName", ItemFrame.media_label.medianame)
                                slide.set("MediaTitle", ItemFrame.media_label.title)
                                slide.set("mediaType", ItemFrame.media_label.selected_mediatype)
                                slide.set("channel", ItemFrame.media_label.channel)
                                slide.set("layer", str(ItemFrame.media_label.layer))
                                slide.set("looping", str(ItemFrame.media_label.looping))
                                slide.set("fade", str(ItemFrame.media_label.fade))
                                slide.set("seek", str(ItemFrame.media_label.seek))
                                slide.set("legnth", str(ItemFrame.media_label.legnth))
                                slide.set("transition", ItemFrame.media_label.transition)
                                slide.set("duration", str(ItemFrame.media_label.duration))
                                slide.set("direction", ItemFrame.media_label.direction)
                                slide.set("tween", ItemFrame.media_label.tween)
                            else:
                                slide.set("MediaName", "")
                            count += 1 
        if source == "Bible":
            fgcolor = ET.SubElement(Verse,"FGcolor")
            fgcolor.text = "white"
            bgcolor = ET.SubElement(Verse, "BGcolor")
            bgcolor.text = "blue"
            for item in settingsXML:
                if item.tag == "template":
                    for preset in item:
                        if preset.get('name') == "Bible":
                            template_list = preset.text

            for x in range(0,len(bibleVerseIndex)):
                slide = ET.SubElement(Verse, 'slide')
                slide.text = bibleVerseIndex[x]
                slide.set('Ref',bibleVerseIndexREF[x])
                slide.set("id", str(count))
                slide.set("template", template_list)#
                slide.set("REF",bibleVerseIndexREF[x])
                slide.set("Header","")
                slide.set("MediaName", "")
                slide.set("timer", "")
                count += 1 

        if source == "slide_edit":
            fgcolor = ET.SubElement(Verse,"FGcolor")
            fgcolor.text = new_fgcolor
            bgcolor = ET.SubElement(Verse, "BGcolor")
            bgcolor.text = new_bgcolor
            self.NewVerseFrm.destroy() 

        self.save_song()                           


    def Delete_verse(self,verse_ID):
        for Verse_colection in songxml:
            if Verse_colection.tag == 'verse':# based on the verseID number the Verse is deleted
                for Verse in Verse_colection:
                    if Verse.get('id') == verse_ID: 
                        Verse_colection.remove(Verse)

            if Verse_colection.tag == "arangement": # the current verseId is deleted from the arangement
                Arangement_list = Verse_colection.text.split(',')
                for VerseID in Arangement_list:
                    if VerseID != verse_ID:
                        try:
                            new_arangement = new_arangement + ',' + VerseID
                        except:
                            new_arangement = VerseID
                        Verse_colection.text = new_arangement
                        print(new_arangement)
        self.save_song()
        self.NewVerseFrm.destroy()

    def save_song(self):
        global songxml
        songname = self.songname
        songout = ET.tostring(element=songxml, encoding='unicode')
        newxml = songout
        test = client.send(DATA_STORE(name=songname, data=str(newxml)))
        self.Load_song(songname)

        APPapplication.Rundown_canvas.configure(scrollregion=APPapplication.Rundown_canvas.bbox("all"))
        APPapplication.Verse_Select_canvas.configure(scrollregion=APPapplication.Verse_Select_canvas.bbox("all"))
        APPapplication.Slide_document_canvas.configure(scrollregion=APPapplication.Slide_document_canvas.bbox("all"))
        print("Song saved!")
################################ end song section
################################ start template section

    def choose_template(self,destination,index,default_template):
        channels = int(settingsXML.get('channels'))
        if destination == "Settings":
            template_list = []
            
            for x in range(0,channels):
                try:
                    template = server_template_preset_index[index].get(x)
                except:
                    template = ""
                template_list.append(template) 
        if destination == "NewXml":
            try:
                self.newsong_frm.destroy()
            except:
                y=None

            template_list = []
            
            for x in range(0,channels):
                try:
                    template = server_template_preset_index[index].get(x)
                except:
                    template = ""
                template_list.append(template) 

        if destination == "Slide":
            template_list = []
            for x in range(0,channels):
                try:
                    template = Slide_edit_frame_index[index].Template_label.get(x)
                except:
                    template = ""
                template_list.append(template)

        if destination == "Xml":
            for item in songxml:
                if item.tag == "template":
                    template_l = item.text
            template_l = template_l.split(',')
            template_list = []
            for x in range(0,channels):
                try:
                    template_list.append(template_l[x])
                except:
                    template_list.append("")
        try:   # Closes any open copys of the template chooser
            self.choose_template_frm.destroy()
        except:
            y=None

        self.choose_template_frm = tk.Tk()
        self.choose_template_frm.title("Select Template")

        p = True
        cnt = 0
        while p:    #this section of code asks caspar for the template list. and if it fails it will ask again up to 20 times
            try:
                temlplatelist = client.send(TLS()).data
            except:
                temlplatelist = None
            if cnt == 20:
                p = False
            if temlplatelist != None:
                p = False
            cnt += 1

        caspar_templatelist_label = tk.Label(self.choose_template_frm, text="All templates on the Caspar server.(click here second!)").grid(column=1,row=0)

        self.caspar_templatelist = tk.Listbox(self.choose_template_frm, width=120, height=40,selectmode="single")
        try:
            for TemplateName in temlplatelist:
                # print(TemplateName)
                TemplateNameB = TemplateName.split('"')
                # print(TemplateNameB)
                try:
                    self.caspar_templatelist.insert(END, TemplateNameB[1])
                except:
                    self.caspar_templatelist.insert(END, TemplateNameB[0])
            self.caspar_templatelist.grid(column=1,row=1,rowspan=15)
        except:
            print("No templates on server!")
            self.choose_templateB(destination, index, "failed")

        self.channel_templates_label = tk.Label(self.choose_template_frm,text="Current Selection(click here first!)\nCaspar templates by channel\nfirst row channel1\nsecond row channel2\n.etc").grid(column=0,row=9)
        self.channel_templates_listbox = tk.Listbox(self.choose_template_frm,selectmode="single",height = 12, width=55)
        self.channel_templates_listbox.grid(column=0,row=10)
        
        self.channel_templates_listbox.bind('<Key>',save_channel_template_index)
        self.caspar_templatelist.bind('<Button-1>',save_channel_template_index)
        self.caspar_templatelist.bind('<Return>', self.add_template_to_listbox)#self.add_template_to_listbox

        for x in range(0, channels):
            self.channel_templates_listbox.insert(END,template_list[x])
        
        self.save_template_selection_butn = tk.Button(self.choose_template_frm, text="Save Changes", command= lambda x1=destination, x2=index,x3=default_template:self.choose_templateB(x1,x2,x3))
        self.save_template_selection_butn.grid(column=1,row=16)

        if destination != "Settings":
            self.load_Preset_template_Label = tk.Label(self.choose_template_frm,text="use a template Preset, or...").grid(column=0,row=0)
            self.load_Preset_template_listbox = tk.Listbox(self.choose_template_frm,selectmode="single",height=4,width=20)
            self.load_Preset_template_listbox.grid(column=0, row=1,rowspan=4)
            presetlist = []
            for template in settingsXML:
                if template.tag == "template":
                    for preset in template:
                        presetlist.append(preset.get('name'))
            for item in presetlist:
                self.load_Preset_template_listbox.insert(END,item) 
            self.load_Preset_template_listbox.bind('<Return>', self.update_Channel_templates_with_Preset)
            self.load_Preset_template_Button = tk.Button(self.choose_template_frm,text="Use selected Preset",command= lambda x1="":self.update_Channel_templates_with_Preset(x1)).grid(column=0,row=5)

        add_button_label = tk.Label(self.choose_template_frm,text="(Then click here!)").grid(column=0,row=14)
        self.select_template_butn = tk.Button(self.choose_template_frm, text="Add template to channel", command= lambda x1="":self.add_template_to_listbox(x1))
        self.select_template_butn.grid(column=0,row=15)

    def update_Channel_templates_with_Preset(self, event):
        channels = int(settingsXML.get('channels'))
        selected_preset = self.load_Preset_template_listbox.get(ACTIVE)
        for template in settingsXML:
            if template.tag == 'template':
                for preset in template:
                    if preset.get('name') == selected_preset:
                        template_list = preset.text
        self.channel_templates_listbox.delete(0,END)
        template_list = template_list.split(',')
        for x in range(0,channels):
            try:
                self.channel_templates_listbox.insert(END,template_list[x])
            except:
                self.channel_templates_listbox.insert(END,"")
    
    def choose_templateB(self, destination, index, default_template):
        global songxml
        channels = int(settingsXML.get('channels'))

        if destination == "Slide":
            template_list = []
            # indexb = Slide_Template_label_index[index].index(ACTIVE) # created a bug, Not sure why I wrote this.

            for x in range(0, channels):
                value = self.channel_templates_listbox.get(x)
                template_list.append(value)
            Slide_edit_frame_index[index].Template_label.delete(0,END)
            for item in template_list:
                Slide_edit_frame_index[index].Template_label.insert(END,item)
            if template_list == default_template:
                Slide_edit_frame_index[index].Template_label.configure(bg="green")
            else:
                Slide_edit_frame_index[index].Template_label.configure(bg="red")

        if destination == "Xml":
            for x in range(0, channels):
                if x == 0:
                    template = self.channel_templates_listbox.get(x)
                else:
                    template = template + ',' + self.channel_templates_listbox.get(x)

            for child in songxml:
                if child.tag == "template":
                    child.text = template
                if child.tag == "verse":
                    for verse in child:
                        for slide in verse:
                            slide.set('template', template)
            self.save_song()

        if destination == "NewXml":
            if default_template == "failed":# no templates in templates folder
                template = "'"
            else:
                for x in range(0, channels):
                    if x == 0:
                        template = self.channel_templates_listbox.get(x)
                    else:
                        template = template + ',' + self.channel_templates_listbox.get(x)

            if index == "":
                songxml = ET.Element('song')
                verse = ET.SubElement(songxml, 'verse')
                arangement = ET.SubElement(songxml, 'arangement')
                print('test11111111')
    

            else:
                songxml = index
                # print(songxml)
                for verse in songxml:
                    if verse.tag == "verse":
                        # print(child.tag)
                        for verses in verse:
                            # print(verses.tag)
                            for slide in verses:
                                if slide.tag == "slide":
                                    # print(slide.text)
                                    slide.set('template',template)
            print(template)
            Stemplate = ET.SubElement(songxml, 'template')
            Stemplate.text = template
            self.save_song()

        if destination == "Settings":
            template_list = []

            for x in range(0, channels):
                template_list.append(self.channel_templates_listbox.get(x))
            server_template_preset_index[index].delete(0,END)

            for item in template_list:
                server_template_preset_index[index].insert(END,item)

        self.choose_template_frm.destroy()

    def add_template_to_listbox(self, event):
        new_template = self.caspar_templatelist.get(ACTIVE)
        template_list = []
        print("channel_templates_active_index: " + str(channel_templates_active_index))
        for x in range(0,int(settingsXML.get('channels')) + 1):
            if x == channel_templates_active_index:
                template_list.append(self.caspar_templatelist.get(ACTIVE))
            else:
                template_list.append(self.channel_templates_listbox.get(x))
        self.channel_templates_listbox.delete(0,END)
        for item in template_list:
            self.channel_templates_listbox.insert(END,item)
####################################### end template section
####################################### start create song section

    def create_new_song(self):
        global songxml
        # global songname

        self.newsong_frm = tk.Tk()
        self.new_song_name_label = tk.Label(self.newsong_frm, text="Name of song(no spaces)")
        self.new_song_name_label.pack()
        self.new_song_name = tk.Entry(self.newsong_frm)
        self.new_song_name.pack()
        new_song_butn = tk.Button(self.newsong_frm, text="Create Song", command=self.create_new_song_B).pack()
        label = tk.Label(self.newsong_frm, text = "or").pack()
        import_propresenter = tk.Button(self.newsong_frm,text="import Proprresenter 6 file",command=self.import_pro6).pack()

        print("new song created")

    def import_pro6(self):
        self.newsong_frm.destroy()
        filename = fd.askopenfilename()
        import_pro6_file(filename)

    def create_new_song_B(self):
        # global songname
        global songxml
        songname = self.new_song_name.get()
        songname.replace(' ', '_')
        self.songname = 'SONGS/' + songname
        self.choose_template("NewXml","","")
        self.newsong_frm.destroy()
######################################## end create song sestion
######################################## start arangement section        
    def delete_Arangement_item(self,index):
        global New_ArangementCol
        widget_frame = delete_widget_frame(Arangement_Item_index, index, self.Arangement_set_grid, self.Arangement_set_canvas, "x", 160)
        New_ArangementCol = widget_frame[0]

    def EditArangement_add(self,VerseName, VerseId, bgcolor, fgcolor,Reload):
        global NewArange_Count
        global New_ArangementCol
        global New_ArangementPos_index

        # Widget_frame = add_widget_frame(Arangement_Item_index, NewArange_Count, New_ArangementPos_index, New_ArangementCol, "Horizontal", self.Arangement_set_grid, self.Arangement_set_canvas, 50, 25, "", 20)
        Widget_frame = add_widget_frame(Arangement_Item_index, NewArange_Count, New_ArangementPos_index, New_ArangementCol, "Horizontal", self.Arangement_set_grid, self.Arangement_set_canvas, 150, 25, "", 20)
        
        Arangement_Item_frame = Widget_frame[0]
        New_ArangementCol = Widget_frame[1]
        New_ArangementPos_index = Widget_frame[2]
        Arangement_Item_frame.VerseId = VerseId
        self.Arangement_set_canvas.configure(scrollregion=self.Arangement_set_canvas.bbox("all")) # updates the scrollbar

        Arangement_Label = tk.Label(Arangement_Item_frame, text=VerseName, fg=fgcolor,bg=bgcolor, width=15)# command= lambda x1=NewArange_Count:self.EditArangement_delete(x1))
        Arangement_Label.pack(side=LEFT)#place(x=(10 + New_ArangementCol), y=20, width=60,height=25)#grid(column=New_ArangementCol, row=0)#
        
    # for sorting
        Arangement_Label.Canvas = self.Arangement_set_canvas # for mousewheel
        Arangement_Label.index = NewArange_Count
        Arangement_Label.Container_index = Arangement_Item_index
        Arangement_Label.bind('<Button-1>', Sort_Widget_start)
        Arangement_Label.bind('<B1-Motion>', Sort_Widget_motion)
        Arangement_Label.bind('<ButtonRelease-1>', Sort_Widget_end)
        Arangement_Label.Canvas = self.Arangement_set_canvas # for mousewheel
        Arangement_Label.orientation = "Horizontal"

        Arangement_X_Button = tk.Button(Arangement_Item_frame, text="X", command= lambda x1=NewArange_Count:self.delete_Arangement_item(x1))
        Arangement_X_Button.pack(side=RIGHT)#.place(x=(5 + New_ArangementCol), y=20, width=20,height=25)#grid(column=New_ArangementCol, row=0)#
        Arangement_X_Button.Canvas = self.Arangement_set_canvas # for mousewheel

        NewArange_Count += 1

        if Reload == True:
            self.EditArangement(True)

    def EditArangement_close(self):
        global songxml
        Arangement_list = []
        for x in range(len(Arangement_Item_index)):
            for item in Arangement_Item_index:
                if item.Position_index == x:
                    if item.state == True:
                        Arangement_list.append(item.VerseId)
        new_arangement_str = List_to_CSV(Arangement_list,',')

        for item in songxml:
            if item.tag == "arangement":
                item.text = new_arangement_str
        self.arangement_frm.destroy()
        self.save_song()

    def Refresh_EditArangement(self,event):
        self.EditArangement(True)

    def EditArangement(self, Reload):
        global NewArange_Count
        global New_ArangementCol
        global Arangement_Item_index
        global New_ArangementPos_index
        New_ArangementCol = 0
        New_ArangementPos_index = 0

        if Reload == False:
            NewArange_Count = 0
            Arangement_Item_index = []
            self.arangement_frm = tk.Tk()
            self.arangement_frm.title("current arangement")
            self.arangement_frm.bind("<F12>", self.Refresh_EditArangement)

            self.close_arangement = tk.Button(self.arangement_frm, text="save", command=self.EditArangement_close)
            self.close_arangement.grid(column=0,row=2)
            for item in songxml:
                if item.tag == "arangement":
                    arangement = item.text
            arangement = arangement.split(',')

        # Creates verse list
        Col = 0
        for item in songxml:
            if item.tag == "verse":
                for verse in item:
                    if verse.tag =="verse":
                        versename = verse.get("name")
                        VerseId = verse.get("id")
                        for color in verse:
                            if color.tag == "FGcolor":
                                fgcolor = color.text
                            if color.tag == "BGcolor":
                                bgcolor = color.text
                        try:
                            self.arangement_versebtn =tk.Button(self.arangement_frm, text=versename, fg=fgcolor, bg=bgcolor, font=('DejaVu Sans', '14'), command = lambda x1=versename, x2=int(VerseId),x3=bgcolor,x4=fgcolor,x5=False: self.EditArangement_add(x1,x2,x3,x4,x5))
                        except:
                            self.arangement_versebtn =tk.Button(self.arangement_frm, text=versename, fg="white", bg="blue", font=('DejaVu Sans', '14'), command = lambda x1=versename, x2=int(VerseId),x3=bgcolor,x4=fgcolor,x5=False: self.EditArangement_add(x1,x2,x3,x4,x5))
                        self.arangement_versebtn.grid(column=Col,row=1)
                        Col +=1



        if Reload == True:
            self.Arangement_set_frame.destroy() 
            arangement = []
            for x in range(len(Arangement_Item_index)):
                try:
                    for item in Arangement_Item_index:
                        if item.Position_index == x:
                            if item.state == True:    
                                item.state = False
                                arangement.append(str(item.VerseId))
                except:
                    y = None

        # begin scrolling frame
        self.Arangement_set_frame = tk.LabelFrame(self.arangement_frm,text=self.songname)
        self.Arangement_set_frame.grid(column=0,row=0,sticky="EW",columnspan=Col)

        SC_canvas = add_scrollable_canvas(self.Arangement_set_frame, "X", APPapplication, Height=40,Width=900,G_Width=40,G_Height=50)
        self.Arangement_set_canvas = SC_canvas[0]
        self.Arangement_set_grid = SC_canvas[1]

        for VerseId in arangement:
            for item in songxml:
                if item.tag == "verse":
                    for verse in item:
                        if verse.tag =="verse":
                            if verse.get("id") == VerseId:
                                VerseName = verse.get("name")
                                for color in verse:
                                    if color.tag == "FGcolor":
                                        fgcolor = color.text
                                    if color.tag == "BGcolor":
                                        bgcolor = color.text
            self.EditArangement_add(VerseName, int(VerseId), bgcolor,fgcolor,False)
################################### end arangement section
                                
    def kill_editverse(self):
        try:
            self.editverse.destroy()
            self.Verse_Select_frame()
        except:
            print("no editverse")

    def kill_Slide_document(self):
        try:
            self.Slide_document.destroy()
        except:
            print("No playlist")
        
################################## start bible section
    def load_bible(self):
        global bibleVersebtnindex
        global bibleVerseLBLindex
        bibleVersebtnindex = []
        bibleVerseLBLindex = []
        self.loadverse_frm = tk.Tk()
        self.loadverse_frm.title("Bible")
        self.loadverse_frm.bind('<Left>', KEY_bible_verse)
        self.loadverse_frm.bind('<Right>', KEY_bible_verse)
        self.loadverse_frm.bind('<Up>', RundownNav)
        self.loadverse_frm.bind('<Down>',RundownNav)
        self.loadverse_frm.bind('<F1>', clearKeys)
        self.loadverse_frm.bind('<F2>', clearKeys)
        self.loadverse_frm.bind('<F3>', clearKeys)
        self.loadverse_frm.bind('<F4>', clearKeys)
        self.loadverse_frm.bind('<F5>', clearKeys)
        self.loadverse_frm.bind('<F6>', clearKeys)
        self.loadverse_frm.bind('<F7>', clearKeys)
        self.loadverse_frm.bind('<F8>', clearKeys)

        if BibleXML == None:
            LoadBible(biblename) # Reloads the BibleXML if it failed at startup.
             

        if BibleXML != None: # loads the bible form
            self.Bible_ref_entry = tk.Entry(self.loadverse_frm)
            self.Bible_ref_entry.grid(column=0,row=0)
            self.Bible_ref_entry.insert(END,"passage e.g. John 3:16")
            self.Bible_ref_entry.bind('<Return>', load__passage)#


            self.Load_verse_frame = tk.LabelFrame(self.loadverse_frm)
            self.Load_verse_frame.grid(column=0,row=2,sticky="EW",columnspan=5)

            self.Load_verse_canvas = Canvas(self.Load_verse_frame, height=900,width=1750) # width=1300, height=900
            self.Load_verse_canvas.pack(side=LEFT, fill=BOTH, expand=1)

            self.Load_verse_button = tk.Button(self.loadverse_frm, text="Load passage", command=self.get_passage).grid(column=2,row=0)
            try:   
                self.Add_Passage_to_Document_button = tk.Button(self.loadverse_frm, text="Save passage",command= lambda x1= versecnt + 1,x2="Bible":self.SaveVerse(x1,x2)).grid(column=3,row=0)
            except:
                y=None
        else:   # The Bible was still not found.
            print("Bible not found!\nCheck if there is a xml Bible under the same directory as caspar_church.\nAlso check the name of the bible under \"Client settings.\"")



    def send_bible_verse(self, index):
        global bibleVersebtnCurrent
        bibleVersebtnCurrent = index
        Send_bible_verse_caspar(index)

    def get_passage(self):
        global reference
        global bibleVersebtnindex
        global bibleVerseLBLindex
        global bibleVerseIndex
        global bibleVerseIndexREF
        global Bible_verse_groups
        global bibleVersebtnOld
        global bibleVersebtnCurrent
        global BibleverseBtnCnt
        global numLinesToSend
        bibleVersebtnCurrent = 0
        bibleVersebtnOld = 0

        textsize = 12
        try:            
            self.Load_verse_frame.destroy()
        except:
            y=None    

        # begin scrolling frame
        self.Load_verse_frame = tk.LabelFrame(self.loadverse_frm)
        self.Load_verse_frame.grid(column=0,row=1,sticky="EW",columnspan=5)

        SC_canvas = add_scrollable_canvas(self.Load_verse_frame, "Y", APPapplication, Height=700,Width=1750)
        self.Load_verse_canvas = SC_canvas[0]
        self.Load_verse_grid = SC_canvas[1]
        
        # destroys the buttons and labels from the last query
        try:
            for x in range(len(bibleVersebtnindex)):
                bibleVersebtnindex[x].destroy()
        except:
            print("button could not be destroyed")

        try:
            for x in range(len(bibleVerseLBLindex)):
                bibleVerseLBLindex[x].destroy()
        except:
            print("label could not be destroyed!")

        print("labels should be destroyed")

        #   Gets the verse range
        reference = scriptures.extract(self.Bible_ref_entry.get())
        referenceStart = reference[0]
        book = referenceStart[0]
        startchapter = referenceStart[1]
        startverse = referenceStart[2]
        endchapter = referenceStart[3]
        endverse = referenceStart[4]
        if startchapter == endchapter:
            singlechapter = True
        else:
            singlechapter = False

        # this section corects the book name to the exact name in xml.
        if book == "Psalms":
            book = "Psalm"

        if book == "I Samuel":
            book = "1 Samuel"
        if book == "II Samuel":
            book = "2 Samuel"

        if book == "I Kings":
            book = "1 Kings"
        if book == "II Kings":
            book = "2 Kings"

        if book == "I Chronicles":
            book = "1 Chronicles"
        if book == "II Chronicles":
            book = "2 Chronicles"

        if book == "I Corinthians":
            book = "1 Corinthians"
        if book == "II Corinthians":
            book = "2 Corinthians"

        if book == "I Thessalonians":
            book = "1 Thessalonians"
        if book == "II Thessalonians":
            book = "2 Thessalonians"
        
        if book == "I Timothy":
            book = "1 Timothy"
        if book == "II Timothy":
            book = "2 Timothy"
        
        if book == "I Peter":
            book = "1 Peter"
        if book == "II Peter":
            book = "2 Peter"
        
        if book == "I John":
            book = "1 John"
        if book == "II John":
            book = "2 John"
        if book == "III John":
            book = "3 John"

        if book == "Revelation of Jesus Christ":
            book = "Revelation"
        


        # Checks to see weather a single verse or a verse range was entered

        Col = 0
        Row = 0
        BibleverseBtnCnt = 0   

        # end2 = False  

        bibleVerseIndex = []
        bibleVerseIndexREF = []
        self.loadverse_frm.book = book
        self.loadverse_frm.startchapter = startchapter
        self.loadverse_frm.startverse = startverse
        self.loadverse_frm.endchapter = endchapter
        self.loadverse_frm.endverse = endverse
        self.loadverse_frm.singlechapter = singlechapter

        # for C_Book in range(startchapter,endchapter)
        for C_Chapter in range(startchapter,endchapter + 1):
            #   Start of the chapter query loop
            if C_Chapter <= endchapter or  C_Chapter == endchapter:#   ends the chapter query early if only a single verse was ordered.
                 #   Start of the verse query loop
                for Cverse in range(startverse, endverse + 1):
                    if Cverse <= endverse or  C_Chapter == endverse:#   ends the verse query early if only a single verse was ordered.
                        #   Start of a single verse query
                        passage = self.load_passage(book, str(C_Chapter), str(Cverse))
                        if passage != "false":
                            split_legnth = int(settingsXML.get('bible_splitLegnth'))
                            numLinesToSend =  int(settingsXML.get('bible_maxlines'))

                            # splits the current verse baised on character length, at nearest word.
                            bible_verse = textwrap.wrap(passage, split_legnth, break_long_words=False)

                            Bible_verse_groups = []
                            cnt = 0
                            bgCNT = 0
                            
                            # creates the verse label
                            label = book + ' ' + str(C_Chapter) + ':' + str(Cverse)
                            self.Bibleverselabel = tk.Label(self.Load_verse_grid, text=label, font=('DejaVu Sans', textsize))
                            self.Bibleverselabel.grid(column = Col, row=Row)
                            self.Bibleverselabel.Canvas = self.Load_verse_canvas # for mousewheel

                            # stores the verse reference in a second array
                            bibleVerseLBLindex.append(self.Bibleverselabel)
                            bvcnt = 0
                            bvmax = len(bible_verse)
                            BVlcnt = 0
                            end11 = False
                            while end11 == False:
                                for x1 in range(0, numLinesToSend):
                                    if bvcnt == bvmax:
                                        end11 = True
                                    elif end11 == False:
                                            if x1 == 0:
                                                    Bible_verse_groups.append(bible_verse[bvcnt])
                                            else:
                                                if bvcnt  <= bvmax:
                                                    Bible_verse_groups[BVlcnt] = Bible_verse_groups[BVlcnt] + '\n' + bible_verse[bvcnt]
                                    bvcnt += 1
                                if end11 == False:
                                    BVlcnt += 1
                            
                            # creates verse buttons and the verse index
                            for linesText in Bible_verse_groups:
                                bibleVerseIndex.append(linesText)
                                bibleVerseIndexREF.append(label)
                                self.bibleVerseLineBtn = tk.Button(self.Load_verse_grid, fg='white', bg='blue', text=linesText, font=('DejaVu Sans', textsize), command=lambda x1=BibleverseBtnCnt:self.send_bible_verse(x1))
                                self.bibleVerseLineBtn.grid(column=Col, row=Row + 1)
                                self.bibleVerseLineBtn.Canvas = self.Load_verse_canvas # for mousewheel

                                bibleVersebtnindex.append(self.bibleVerseLineBtn)
                                BibleverseBtnCnt += 1
                                Col += 1
                                if Col == 5:
                                    Row += 2
                                    Col = 0
                            if Col == 5:
                                    Row += 2
                                    Col = 0

                        else:
                            print("Passage is out of range!")

    #      gets individual verse from xml Bible 
    def load_passage(self ,bookName, chapterNum, verseNum):#,book,chapter,verse
        for book in BibleXML:
            if book.get('bname') == bookName:
                for chapter in book:
                    if chapter.get('cnumber') == str(chapterNum):
                        for verse in chapter:
                            if verse.get('vnumber') == str(verseNum):
                                return verse.text

        else:
            return "false"  
############################## end bible section

    def _bound_to_mousewheel(self, event):# this function attempts to reconfigure the scrollregion of every most scrollable frames
        widget = event.widget
        widget.Canvas.bind_all("<MouseWheel>", self._on_mousewheel) 
        try:
            APPapplication.Rundown_canvas.configure(scrollregion=APPapplication.Rundown_canvas.bbox("all"))
        except:
            y=None

        try:
            APPapplication.Verse_Select_canvas.configure(scrollregion=APPapplication.Verse_Select_canvas.bbox("all"))
        except:
            y=None

        try:
            APPapplication.Slide_document_canvas.configure(scrollregion=APPapplication.Slide_document_canvas.bbox("all"))
        except:
            y=None

        try:
            APPapplication.Media_select_canvas.configure(scrollregion=APPapplication.Media_select_canvas.bbox("all"))
        except:
            y=None

        try:
            APPapplication.Verseedit_canvas.configure(scrollregion=APPapplication.Verseedit_canvas.bbox("all"))
        except:
            y=None
        
        try:
            APPapplication.Arangement_set_canvas.configure(scrollregion=APPapplication.Arangement_set_canvas.bbox("all"))
        except:
            y=None

    def _unbound_to_mousewheel(self, event):
        widget = event.widget
        widget.Canvas.unbind_all("<MouseWheel>") 

    def _on_mousewheel(self, event):
        widget = event.widget
        if widget.Canvas.XY == "Y":
            widget.Canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        if widget.Canvas.XY == "X":
            widget.Canvas.xview_scroll(int(-1*(event.delta/120)), "units")

    def send_lyric(self, index):
        global VerseLineBtnIndex
        global enable_timer
        enable_timer = True
        VerseLineBtnIndex = index
        Send_Verse(index)
        verseline_button_indicator()

    # def startEditSong(self):
    #     global Edit
    #     # load=tk.Button(self)
    #     # load["text"] = "load song"
    #     # load.pack(side="top")
    #     # load["command"] = self.load_song

    #     # if Edit == False:
    #         # Edit = True        
    #     self.song_entry.insert(tk.END, "``verse1\n``verse2\n``verse3")

    #     # else:
    #         # print("test")
    #     # else:
    #     #     self.close_song.destroy()
    #     #     Edit = False
    #     test123 = self.song_entry.get(1.0, 999.999)
    #     test2 = test123.split("\n")
    #     print(test2[0])
    #     print(test2[2])

    # def closeSong(self):
    #     self.song_entry.destroy()
    #     self.close_song.destroy()


root = tk.Tk()
# root.geometry('1024x768')#codechange11
# root.grid_rowconfigure(0, weight=1)
# root.grid_rowconfigure(1, weight=3)
# root.grid_columnconfigure()

app = Application(master=root)
app.mainloop()
# string1 = "Just as I am, with out one plea"
# string2 = "But that thy blood was shed for me"
# use_template(1, 20, "EXAMPLE", string1, string2)

