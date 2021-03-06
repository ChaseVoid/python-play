#!/usr/bin/env python
#
#       playCopy 1.0 (python script)
#       
#       Copyright 2009 Vladimir Kolev <admin@vladimirkolev.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#	
#	Special thanks to Umang <umang.me@gmail.com> for the changes in the script.
#	See section 4. in INSTALL file for the changes
#


import os
import commands
# python-dbus used for getting the information from Audaicous
import dbus

# Set show_not to 0 to disable the notifications
show_not = 1

def cur_song():
	"""Attempts to find the name of the song playing by checking which music player is running and retreiving the song name from the application.
	
	Players currently supported: Rhythmbox, mocp, Exaile, Banshee, Audacious"""
	if "banshee" in os.popen('ps -A | grep banshee').readline():
		# Get the banshee artist and title and replace the unneccessery tiles from the string
		artist = os.popen('banshee --query-artist').readline().replace('artist: ', '').replace('\n', '')
		title = os.popen('banshee --query-title').readline().replace('title: ', '').replace('\n', '')
		song = "%s - %s" % (artist, title)
	elif "exaile" in os.popen('ps -A | grep exaile').readline():
		# Get the exaile artist and title and replace the unneccessery tiles from the string
		artist = os.popen('exaile --get-artist').readline().replace('artist: ', '').replace('\n', '')
		title = os.popen('exaile --get-title').readline().replace('title: ', '').replace('\n', '')
		song = "%s - %s" % (artist, title)
	elif "rhythmbox" in os.popen('ps -A | grep rhythmbox').readline():
		# Get the rhythmbox current playing information and set it to artist
		song = os.popen('rhythmbox-client --print-playing').readline().replace('\n', '')
	elif "mocp" in os.popen('ps -A | grep moc').readline():
		# Get the information from mocp
		info = commands.getoutput("mocp --info").splitlines()
		if info == ["State: STOP"]:
			#If mocp is stopped, then change the artist to Nothing to show
			song = "moc is stopeed"
		else:
			# If there is a song information split it and formatid for the final string
			artist = info[3].replace('Artist:', '')
			title = info[4].replace('SongTitle:', '')
			song = "%s - %s" % (artist, title)
	elif "audacious" in os.popen('ps -A | grep audacious').readline():
		 # initialise the dbus
		 session_bus = dbus.SessionBus()
		 # create two proxies 
		 # proxy_obj1 gets integer for the current playing track in the playlist
		 proxy_obj1 = session_bus.get_object('org.mpris.audacious', '/TrackList')
		 selecter = dbus.Interface(proxy_obj1, 'org.freedesktop.MediaPlayer')
		 # store the integer for the playing track so to be sended to proxy_obj2
		 ct = selecter.GetCurrentTrack()
		 # proxy_obj2 retrieves the title of the current playing track
		 proxy_obj2 = session_bus.get_object('org.mpris.audacious', '/org/atheme/audacious')
		 player = dbus.Interface(proxy_obj2, 'org.atheme.audacious')
		 # Store the title in the song variable
		 song = player.SongTitle(ct)
	elif "listen" in os.popen('ps -A | grep listen').readline():
		# Get the current song from the commandline interface
		info = commands.getoutput("listen -c")
		if info == ["No song playing"]:
			# If No song playing create song variable with "Listen player is paused"
			song = "Listen player is not playing"
		else:
			# if Listen is playing then create the song variable with the information:
			song = info.replace("\n", "")
	elif "quodli" in os.popen('ps -A | grep quodli').readline():
		# Get the current playing song from the command line
		info = os.popen('quodlibet --print-playing').readline()
		song = info.replace('\n', '')
	elif "bluemindo" in os.popen('ps -A | grep bluemin').readline():
		# Get the current playing song from the command line
		info = os.popen('bluemindo --current').readline()
		song = info.replace('\n', '')
	elif "jajuk" in os.popen('ps -A | grep jajuk').readline():
		session_bus = dbus.SessionBus()
		proxyobj1 = session_bus.get_object('org.jajuk.dbus.DBusSupport', '/JajukDBus')
		selected = dbus.Interface(proxyobj1, 'org.jajuk.services.dbus.DBusSupport')
		song = selected.current()
	else:
		if show_not == 1:
			import pynotify
			pynotify.init("playCopy")
			ne = pynotify.Notification("playCopy", "\nNo supported player running", "error")
			ne.show()
	return song

if __name__ == "__main__":
	import pygtk
	import gtk	

	nowplaying = " #nowplaying"
	# Define the clipboard
	clipboard = gtk.clipboard_get()
	# Get the song name from cur_song(), copy the string to the clipboard and store it
	clipboard.set_text(cur_song() + nowplaying)
	clipboard.store()
	
	if show_not == 1:
		try:
			import pynotify
			if pynotify.init("playCopy"):
				n = pynotify.Notification("playCopy", "\n%s" % clipboard.wait_for_text(), "audio-volume-medium")
				n.show()
				
		except:
			print "You don't have pynotify installed!"
    
#	try:
#		import twitter
#		api = twitter.Api()
#		api = twitter.Api(consumer_key='consumer_key', consumer_secret='consumer_secret', access_token_key='access_token', access_token_secret='access_token_secret') 
#		txt = clipboard.wait_for_text()
#		update = api.Update(txt)
#		print "test: " + txt
#	
#	except:
#		print "Twitter not initiated!"


