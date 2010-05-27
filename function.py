#!/usr/bin/env python
# -*- coding: utf8 -*-

#	This file is part of CatchX.
#
#	CatchX is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	CatchX is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with CatchX.  If not, see <http://www.gnu.org/licenses/>.


import os
import xmlrpclib
import time
import thread
from maps import potsdam as the_map

game_started = False
		
def get_gamedata(s, password, name, room, window):
	room = s.roomreq(name, room, password)
	if room == 'running':
		print "Game is already running"
		thread.start_new_thread(blink_window, (window,))
		return "err_running"
	if room == 'password':
		print "Wrong password or the room doesn't exist"
		thread.start_new_thread(blink_window, (window,))
		return "err_login"
	playerid = room[0]
	roomid = room[1]
	print("Got assigned playerid #" + str(playerid))
	players = s.get_players(playerid)
	#print "Players on the server: " + str(players)
	return (playerid,players,roomid)
	
def load_maingui(cliwindow, players, playerid, version, s): #This is the most complex GUI, the maingui...
#def load_maingui(start):
	#cliwindow = start.cliwindow
	#players = start.gdata[1]
	#playerid = start.gdata[0]
	global vpan, startbox, mapbox
	
	
	def start_game(self): #copied hier for testing prps
		global started
		if started == True:
			chat_update("\n* The game is already started!")
			return
		started = True
		cmd = s.startgame(playerid)
		busbutton.set_sensitive(True)
		trambutton.set_sensitive(True)
		taxibutton.set_sensitive(True)
		if cmd[1] == playerid:
			shipbutton.set_sensitive(True)
			bankrobb.set_sensitive(True)
			simpletheftb.set_sensitive(True)
			grandtheftb.set_sensitive(True)
			burglaryb.set_sensitive(True)
			chat_update("* You are the Mister X")
			chat_update("* It's your turn")
		else:
			chat_update("* " + cmd[0] + " is the Mister X")
			chat_update("* It's " + cmd[0] + "'s turn")

		vpan.remove(startbox)
		vpan.add(mapbox)
		vpan.show_all()
	
	def destroy_room(self):
		return #As this function is not implemented @ the server yet ;)
		cmd = s.roomdestroy(pid)
		chat_update("\n" + cmd)
		
	def quit_cb(self):
		s.playerleave(playerid)
		#print "RPoints = " + str(rpoints)
		print 'Quitting program'
		gtk.main_quit()
	
	cliwindow.maximize() #We need the complete space
	size = cliwindow.get_size() #Now get the size of the maximized window
	print "WSize = " + str(size)
	uppersize = int((size[0] / 95) *100)
	print uppersize
	print "MapPoints = " + str(map.points)
	ui = '''<ui>
	<menubar name="MenuBar">
		<menu action="File">
			<menuitem action="Start"/>
			<menuitem action="Destroy"/>
			<separator/>
			<menuitem action="Quit"/>
		</menu>
		<menu action="Help">
			<menuitem action="About"/>
		</menu>
	</menubar>
	</ui>'''
	
	uimanager = gtk.UIManager()
	accelgroup = uimanager.get_accel_group()
	cliwindow.add_accel_group(accelgroup)
	
	actiongroup = gtk.ActionGroup('UIManagerExample')
	
	actiongroup.add_actions([('Quit', gtk.STOCK_QUIT, '_Quit', None,
		'Quit CatchX', quit_cb),
		('Start', gtk.STOCK_APPLY, '_Start Game!', None, 'Start Game!', start_game),
		('Destroy', gtk.STOCK_STOP, '_Destroy Room', None, 'Destroy Room', destroy_room),
		('File', None, '_File'),
		('Help', None, '_Help'),
		('About', gtk.STOCK_ABOUT, '_About', None,
		'About', about_window)])
	actiongroup.get_action('Quit').set_property('short-label', '_Quit')
	uimanager.insert_action_group(actiongroup, 0)
	uimanager.add_ui_from_string(ui)
	menubar = uimanager.get_widget('/MenuBar')
	
	clibox = gtk.VBox(False, 0)
	cliwindow.add(clibox)
	
	clibox.pack_start(menubar, False)
	
	mapbox = gtk.HBox(False, 0)
	
	toolbox = gtk.HBox(False, 0)
	
	leftdnbox = gtk.HBox(False, 0)
	
	rightdnbox = gtk.VBox(False, 0)
	
	buttonbox = create_buttonbox()
	mapbox.pack_start(buttonbox, False, False, 0)
	
	image = gtk.Image()
	image.set_from_file("img/map.png")
	pixelsize = image.get_pixbuf() # get the size of the picture to adjust the Layout size
	pixelwidth = pixelsize.get_width()
	pixelheight = pixelsize.get_height()

	global layout, i1
	#Layout and Scrollbar settings
	layout = gtk.Layout()
	vadjust = layout.get_vadjustment()
	hadjust = layout.get_hadjustment()
	vadjust.step_increment = 10
	hadjust.step_increment = 10
	layout.set_size(pixelwidth, pixelheight)
	vscrollbar = gtk.VScrollbar(vadjust)
	hscrollbar = gtk.HScrollbar(hadjust)
	vscrollbar.show()
	hscrollbar.show()
	layout.set_events(gtk.gdk.BUTTON_PRESS_MASK)
	layout.connect("button_press_event", button_press)
	layout.put(image, 0, 0)
	
	i1 = gtk.Image()	
	i1.set_from_file("img/figures/green.png")
	layout.put(i1, 348, 260)
		
	#packing the layout and the scrollbars in the Table
	table = gtk.Table(2, 2, 0)
	table.attach(layout, 0, 1, 0, 1, gtk.EXPAND|gtk.FILL, gtk.EXPAND|gtk.FILL, 0, 0)
	table.attach(vscrollbar, 1, 2, 0, 1, 0, gtk.EXPAND|gtk.FILL, 0, 0)
	table.attach(hscrollbar, 0, 1, 1, 2, gtk.EXPAND|gtk.FILL, 0, 0, 0)
	mapbox.pack_start(table)
	
	xbar = gtk.ProgressBar()
	xbar.set_orientation(gtk.PROGRESS_BOTTOM_TO_TOP)
	xbar.set_fraction(0.35)
	mapbox.pack_end(xbar, False, False, 0)
	mapbox.pack_end(gtk.VSeparator(), False, False, 3)
	
	chatframe = gtk.Frame()
	rightdnbox.add(chatframe)
	
	#label3 = gtk.Label(str)
	#label3.set_text("Right Toolbox")
	#chatframe.add(label3)
	global textbuffer, dtext, textview
	textview = gtk.TextView()
	textbuffer = textview.get_buffer()
	textview.set_editable(False)
	dtext = "* Welcome to CatchX v%s" % str(version)
	textbuffer.set_text(dtext)
	chatframe.add(textview)

	
	downerchat = gtk.HBox(False, 0)
	rightdnbox.pack_end(downerchat, False, False, 0)

	
	chatentry = gtk.Entry()
	downerchat.pack_start(chatentry, True, True, 0)
	
	def sendmsg(widget):
		if chatentry.get_text() <> "":
			msg = chatentry.get_text()
			chatentry.set_text('')
			s.chat(playerid, msg)
				
	sendbutton = gtk.Button("-> Send")
	sendbutton.connect("clicked", sendmsg)
	sendbutton.set_sensitive(False)
	
	def changebuttonstate(widget):
		if chatentry.get_text() <> "":
			sendbutton.set_sensitive(True)
		else:
			sendbutton.set_sensitive(False)
	
	chatentry.connect("changed", changebuttonstate)
	chatentry.connect("activate", sendmsg)
	
	downerchat.pack_end(sendbutton, False, False, 0)
	
	#The user-list
	global liststore
	liststore = gtk.ListStore(str, str, str)
	treeview = gtk.TreeView(liststore)
	
	tvcolumn = gtk.TreeViewColumn('Name')
	tvcolumn1 = gtk.TreeViewColumn('Money')
	tvcolumn2 = gtk.TreeViewColumn('PID')
	
	treeview.append_column(tvcolumn)
	treeview.append_column(tvcolumn1)
	treeview.append_column(tvcolumn2)
	
	#print players
	print players
	global iter
	iter = ()
	for name in players:
		iter += (liststore.append([name[0], "--", name[1]]),)
	
	cell = gtk.CellRendererText()
	cell1 = gtk.CellRendererText()
	cell2 = gtk.CellRendererText()
		
	#tvcolumn.pack_start(cellpb, False)
	tvcolumn.pack_start(cell, True)
	tvcolumn1.pack_start(cell1, True)
	tvcolumn2.pack_start(cell2, True)
	
	tvcolumn.set_attributes(cell, text=0)
	tvcolumn1.set_attributes(cell1, text=1)
	tvcolumn2.set_attributes(cell2, text=1)
	
	#userlist scrollbar
	useradjust = treeview.get_vadjustment()
	useradjust.step_increment = 10
	userscrollbar = gtk.VScrollbar(useradjust)
	
	treeview.set_search_column(0)
	tvcolumn1.set_sort_column_id(0)
	leftdnbox.add(treeview)
	leftdnbox.pack_end(userscrollbar, False, False, 1)
	
	#the initial start info
	startbox = gtk.VBox(False, 0)
	image = gtk.Image()
	image.set_from_file("img/logo.png")
	startbox.add(image)
	info = gtk.Label("""To start the game, press File -> Start game!\nBut wait for the other players first, when the game is started, no new players can join the room!""")
	startbox.add(info)
	
	
	vpan = gtk.VPaned()
	#vpan.add1(mapbox)
	vpan.add1(startbox)
	vpan.add2(toolbox)
	clibox.pack_start(vpan)
	hpan = gtk.HPaned()
	hpan.add1(leftdnbox)
	hpan.add2(rightdnbox)
	toolbox.add(hpan)
	
	vpan.set_position(uppersize)
	hpan.set_position(200)
	
	cliwindow.show_all()

def button_press(widget, event):
	global rpoints
	print "Mapclick = " + str(event.x) + str(event.y)
	#rpoints[event.x] = event.y
	for xwert, ywert in map.points.items():
		if (-10 < (event.x - xwert) < 10) and (-10 < (event.y - ywert) < 10):
			layout.move(i1, xwert - 16, ywert - 40)
			print "Onitem = Yes"
			return True
	return False
	
def chat_update(text):
	global textbuffer, dtext
	dtext += "\n" + text
	textbuffer.set_text(dtext)
	textview.scroll_mark_onscreen(textbuffer.get_insert())

def keepalive(s,pid):
	time.sleep(1)
	i = 0
	while(True): #infinite loop
		i += 1
		try:
			command = s.keepalive(pid)
		except:
			print "Lost connection to the Server!"
			print "Quitting program!"
			gtk.main_quit()
		if command != "none":
			command = command.split("><");
			for cmd in command:
				cmd = cmd[4:]
				cmd = cmd.split("<>");
				print cmd
				if cmd[0] == 'chatmsg':
					chat_update(str(cmd[1]) + ": " + str(cmd[2]))
				if cmd[0] == 'playerjoin':
					chat_update("* " + cmd[1] + " joined the room")
					liststore.append([cmd[1], "--"])
				if cmd[0] == 'playerleave':
					chat_update("* " + cmd[1] + " has left")
					liststore.remove(iter[cmd[1]])
			
		time.sleep(0.20)
