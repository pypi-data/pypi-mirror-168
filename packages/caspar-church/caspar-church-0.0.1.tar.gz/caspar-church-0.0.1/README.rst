=======================================
Release notes for CasparCG Church 1.2.1
=======================================

Now Tested with CasparCG v2.3 on Windows
========================================

Features still under development:
---------------------------------
  * In the amcp_pylib Package An ADD STREAM command does not work(This is for streaming a channel to VLC for Preview .Etc).
  * Intigrating asyncio comand loops.

Known issues:
-------------
  * although theoretically multiple copy's of CasparCG church can be run on different machines on the LAN, each managing different aspects of the service. Currently CasparCG church(Client) can only connect to a CasparCG(server) on the same machine. However if you want a second client managing motion graphics it can be done using the official CasparCG client.
  * Note: When searching for a bible passage some 3 character bible abbreviations will not work at the moment. for instance "exo 20:1" instead use 4 character abbreviations, "exod 20:1"


Operational overview:
---------------------
 CasparCG Church is a client for CasparCG.
 when you run CasparCG Church the following wil occur.
 The BibleXML will be loaded. (This is specified in the installation instructions The BibleXML needs to be stored in the same Folder as Caspar_Church.py)
 (Note: the .ftd files listed in this document are "stored data" files on the Caspar server)
 Server_settings.ftd is retreved from the CasparCG server, this xml contains presets specific to this server.(this file is generated if none exists.)
 Rundown.ftd is loaded from the server, this xml contains the data needed to RE-generate the rundown if a rundown has been saved.
 Thumbnails are loaded from the server and stored locally in Thumbnail.xml(This to decrees loading time on future startups.)
 The "Master media List" is loaded, the main reason for making this was to debug thumbnails, however it is also useful for testing video and still images. video/stills will be played on channel 1, layer 10, not looping.
 
 After loading a song, when you click a slide. all the details of the current slide are saved as current_data.ftd. Then for each channel a CG_ADD command is issued to apply the template.
 if the next slide played uses the same template as the previous template. a CG_UPDATE command is issued instead, this is to increase responsiveness

 if the slide you clicked has media attached that media will be played on the appropriate channel or channels on the specified layer(Note: to play media on multiple channels at once enter the channels in CSV format I.E. 1,2 2,3 1,2,3 .etc).

 if the slide clicked has a timer attached. the next slide will play after the specified seconds.

 The slide text will be sent as f0 through whatever is specified in "Bible, max lines per slide" under settings.

 The next slide will be sent as b0 through "Bible, max lines per slide".

 if the slide contains header information, that is sent as h0 to infinity.

 if the slide contains a reference, that will be sent as ref.

      Note: all the aforementioned data is stored automatically as current_data.

 If a video is played, the time the video should finish is stored as the variable "Video_Seconds". when f7 is pressed a countdown timer will be displayed showing the remaining time, on the stage display channel.

 You can click and drag the items in the rundown to change their agangement. This also works in the song arangement.

Hotkeys:
========
  * **General:**
  
    * **F1:** Clears all channels
    * **f2:** Clear all templates on layer 20
    * **f3:** Clear all Media on layer 10(video default)
    * **f6:** Fade to black all channels,(layer 10 only) useful when using a trimmed media file.\
    * **f7:** Displays the video countdown on the stage display channel (The last channel, if 3 channels are configured stage display is channel 3) on layer 21.
    * **f8:** Pause and resume any movie played on layer 5of any channel( NOTE: the PAUSE command is Broken in amcp_pylib.Basic module; it actually sends a **PLAY** command, 5 second fix in line 40 of basic.py).
    * **f9:** streaming test code(not functional) also test code for playing a webcam.
    * **f11:** Caspar info test code(not functional, experiment to query what is playing)
    * **f12:** additional test code depreciated, extra
    * **Up:** Play Previous rundown item
    * **Down:** Play next Rundown item
    * **Left:** Play previous slide
    * **Right:** Play next slide

  * **While in the verse editor:**
    * **Ctrl+r** Split the current slide into multiple slides, A blank line is used for splitting.

      example:

      line1

      line2

      line3

      line4

    * **Ctrl+d** Condense the text of all the slides of the current verse into one slide(note this is for the slide text only Reference, Header, media .Etc is all lost when verse is saved).

  * **While in chose media:**
    After selecting the desired media file hit enter to display the thumbnail(if the media file is a MOVIE The trim media bar will be displayed).

    **Trim media hotkeys**: (Note: preview is only available at this time via a stream consumer on the server and not in the client itself)
    * **Note**: on CasparCG server version 2.1 NOT 2.1 Beta2, trimming a movie will only be accurate to within a few seconds not to the exact frame. on a short clip (under 20 minutes) trim points are accurate to within one second. on a longer clip(50 minutes or longer) the accuracy is within 5 seconds. I recommend using **f6** to end a clip early if this is a issue .
    * **q** and **e** adjusts the start frame
    * **w** plays the first 30 frames after the start frame, The first frame played is where the video will start.
    * **a** and **d** adjusts the length
    * **s** plays the last 30 frames, The final frame played is where the video will end.

Installation instructions for CasparCG church.
==============================================

 Note: these instructions assume you are already familiar with CasparCG and already have CasparCG installed.

 From your Python Console:

 **pip install Carpar_chruch**

 **click the settings button on the main form.**

 You will need to enter the biblename (optional), server ip and server port.

 enter the number of channels on your caspar server (this is crucial for working with multiple channels).

 if you use the bible template I have provided set **"Bible, max line legnth"** to **45** and **"Bible, max lines per slide"** to **4.**

 you will notice there is a template profile named "bible". This is the profile used on bible verses, you will need to select your desired templates before sending bible verses.

 you will notice a button named add verse profiles here you can save button colors and versenames presets. (accessible from the edit verse form simply click a **verse name** and hit **enter**).

 you are now ready to create a song or do whatever your worship leader insists. :D
 