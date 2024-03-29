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
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSEs.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with CatchX.  If not, see <http://www.gnu.org/licenses/>.

import pygtk
import gobject
import gtk
import math
import uimap
import time
import locale
import gettext
from modules import connector as connector
from modules import playerobj as playerobj

gettext.bindtextdomain('catchx', 'locale')
gettext.textdomain('catchx')
_ = gettext.gettext

class AboutDialog(gtk.AboutDialog):
	
	def __init__(self):
		gtk.AboutDialog.__init__(self)
		self.set_name(_("CatchX"))
		self.set_copyright(_("© 2009-2010 CatchX Team"))
		self.set_website(_("http://www.catchx.net"))
		self.set_license("""CatchX is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

CatchX is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSEs.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with CatchX.  If not, see <http://www.gnu.org/licenses/>.
""")
		self.set_comments(_("“Quick, before it's too late!”"))
		self.set_authors((("Lukas Martini (Main developer)"), ("Raphael Michel (Main developer)"), ("Benjamin Richter (Quality assurance)"), ("Phillip Thelen (Contributor)")))
		self.set_artists((("Robin Eberhard"),))
		self.set_logo(gtk.gdk.pixbuf_new_from_file("img/logo.png"))
		self.set_wrap_license(True)

class ActionsWidget(gtk.VBox):

	actions = (_('bus'), _('tram'), _('taxi'), _('ship'),_('bank robbery'), _('simple theft'), _('grand theft'), _('burglary'))

	def __init__(self):
		gtk.VBox.__init__(self)
			
		# ———— Actions ————
		for t in self.actions:
			box = gtk.VBox()
			box.pack_start(gtk.image_new_from_file('img/travelicons/{0}.png'.format(t)), fill=False)
			box.pack_end(gtk.Label(t.title()), expand=False, fill=False)
			
			btn = gtk.Button()
			btn.add(box)		
			self.pack_start(btn, fill=False, expand=False)

class ChatWidget(gtk.VBox):

	def __init__(self):
		gtk.VBox.__init__(self)
		
		self.chat_box = gtk.TextView()
		self.chat_buffer = self.chat_box.get_buffer()
		self.chat_box.set_editable(False)
		self.chat_text = _(" * Welcome to CatchX!")
		self.chat_buffer.set_text(self.chat_text)
		
		self.pack_start(self.chat_box, expand=True, fill=True)		
		hbox = gtk.HBox()
		self.pack_end(hbox, expand=False)
		
		self.msg_entry = gtk.Entry()
		hbox.pack_start(self.msg_entry)
		
		self.send_btn = gtk.Button(_('Send'))
	
	#-> This produces REALLY extreme CPU usage of Catchx, dunno why
	#	self.send_btn = gtk.Button()
	#	hbox = gtk.HBox()
	#	image = gtk.Image()
	#	image.set_from_stock(gtk.STOCK_GO_FORWARD, 5)
	#	label = gtk.Label('Send')
	#	hbox.add(image)
	#	hbox.add(label)
	#	self.send_btn.add(hbox)
		hbox.pack_end(self.send_btn, expand=False, fill=False)

class PlayerlistWidget(gtk.VBox):

	def __init__(self):
		gtk.VBox.__init__(self)

		# create a TreeStore with one string column to use as the model
		self.listStore = gtk.ListStore(str,str)

		

		treeView = gtk.TreeView(self.listStore)

		nameColumn = gtk.TreeViewColumn('Name')
		moneyColumn = gtk.TreeViewColumn('Money')

		treeView.append_column(nameColumn)
		treeView.append_column(moneyColumn)

		nameCell = gtk.CellRendererText()
		moneyCell = gtk.CellRendererText()

		nameColumn.pack_start(nameCell, True)
		moneyColumn.pack_start(moneyCell, True)

		nameColumn.add_attribute(nameCell, 'text', 0)
		moneyColumn.add_attribute(moneyCell, 'text', 1)

		# make it searchable
		#self.treeview.set_search_column(0)

		# Allow sorting on the column
		nameColumn.set_sort_column_id(0)
		moneyColumn.set_sort_column_id(1)

		self.add(treeView)

class GameMainMenuBar(gtk.MenuBar):

	def __init__(self):
		gtk.MenuBar.__init__(self)

		# Game
		game_menu = gtk.Menu()
		game_item = gtk.MenuItem(_('Game'))
		game_item.set_submenu(game_menu)
		self.append(game_item)

		self.game_start = gtk.MenuItem(_('Start game'))
		game_menu.append(self.game_start)

		self.game_stop = gtk.MenuItem(_('Destroy room'))
		self.game_stop.set_sensitive(False)
		game_menu.append(self.game_stop)
		
		self.game_leave = gtk.MenuItem(_('Leave CatchX'))
		game_menu.append(self.game_leave)
		
		#View-Menu
		view_menu = gtk.Menu()
		view_item = gtk.MenuItem(_('View'))
		view_item.set_submenu(view_menu)
		self.append(view_item)
		
		self.view_chat = gtk.CheckMenuItem(_('Show Chat'))
		self.view_chat.set_active(True)
		view_menu.append(self.view_chat)
		
		self.view_playerlist = gtk.CheckMenuItem(_('Show Playerlist'))
		self.view_playerlist.set_active(True)
		view_menu.append(self.view_playerlist)

		#MisterX-Menu
		misterx_menu = gtk.Menu()
		misterx_item = gtk.MenuItem(_('Mister X'))
		misterx_item.set_submenu(misterx_menu)
		self.append(misterx_item)
		
		self.misterx_bankrobbery = gtk.MenuItem(_('Bank robbery'))
		self.misterx_bankrobbery.set_sensitive(False)
		misterx_menu.append(self.misterx_bankrobbery)
		
		self.misterx_stheft = gtk.MenuItem(_('Simple theft'))
		self.misterx_stheft.set_sensitive(False)
		misterx_menu.append(self.misterx_stheft)
		
		self.misterx_gtheft = gtk.MenuItem(_('Grand theft'))
		self.misterx_gtheft.set_sensitive(False)
		misterx_menu.append(self.misterx_gtheft)
		
		self.misterx_burglary = gtk.MenuItem(_('Burglary'))
		self.misterx_burglary.set_sensitive(False)
		misterx_menu.append(self.misterx_burglary)

		# Help
		help_menu = gtk.Menu()
		help_item = gtk.MenuItem(_('Help'))
		help_item.set_submenu(help_menu)
		self.append(help_item)
		

		self.about = gtk.MenuItem(_('About'))
		help_menu.append(self.about)
		
	

class GameWindow(gtk.Window):

	def ev_about(self, ev):
		dlg = AboutDialog()
		dlg.show_all()
		dlg.run()
		dlg.hide()

	def ev_start(self, ev):
		self.connection.cmd("start_game", (self.connection.session,))
		self.menu_bar.game_start.set_sensitive(False)
		self.menu_bar.game_stop.set_sensitive(True)
		#self.actions.btn.set_sensitive(True)
		#self.vpan.add1(self.up_hpan)

	def ev_leave(self, ev):
		self.connection.cmd("logout", (self.connection.session,))
		self.connection.session = None
		gtk.main_quit()

	def ev_stop(self, ev):
		print "Not implemented yet (And probably it'll never be)."
		#self.connection.cmd("stop_game", (self.connection.session,))
		#self.menu_bar.game_start.set_sensitive(True)
		#self.menu_bar.game_stop.set_sensitive(False)

	def ev_toggle_chat(self, ev):
		if ev.get_active():
			self.cplbox.show()
		else:
			self.cplbox.hide()

	def ev_toggle_playerlist(self, ev):
		if ev.get_active():
			self.playerlist.show()
		else:
			self.playerlist.hide()
		
	def chat_update(self, text):
		self.chat.chat_text += "\n " + text
		self.chat.chat_buffer.set_text(self.chat.chat_text)
		self.chat.chat_box.scroll_mark_onscreen(self.chat.chat_buffer.get_insert())


	def send_message(self, widget):
		self.connection.cmd("say", (self.connection.session, self.chat.msg_entry.get_text()))
		self.chat.msg_entry.set_text('')

	def logged_in(self, connection):
		self.connection = connection
		self.connection.run()
		
		playerlist = self.connection.cmd("get_playerlist", (self.connection.session,))
		for i in playerlist:
			if not i[0] in self.connection.players:
				tplayer  = playerobj.Player(i[0], i[1]) # PID, Nick
				self.connection.players[i[0]] = tplayer
				tplayer.listStoreIter = self.playerlist.listStore.append([i[1], "{0}€".format(tplayer.money)])
	
	def __init__(self):
		gtk.Window.__init__(self)

		# ———— Main Box ————
		main_box = gtk.VBox()
		self.add(main_box)

		# ———— Menu ————
		self.menu_bar = GameMainMenuBar()
		main_box.pack_start(self.menu_bar, expand=False)

		# ———— Vpan ————
		self.vpan = gtk.VPaned()
		main_box.pack_end(self.vpan)

		# ———— Map/Toolbox ————
		self.up_hbox = gtk.HBox()
		self.vpan.add1(self.up_hbox)
		
		# ———— Set the right size for the chat/playerlist ————
		size = self.get_size()
		uppersize = 450 #size returns incorrect values and this doesnt seem to do anything -.-
		self.vpan.set_position(uppersize)
		
		# ———— Actions Menu ————
		self.actions = ActionsWidget()
		self.up_hbox.pack_start(self.actions, fill=False, expand=False)
		
		# ———— Map ————
		self.map = uimap.MapWidget('img/map.png', self)
		self.map.set_size_request(-1, size[1] + 100)
		self.up_hbox.pack_end(self.map, fill=True, expand=True)

		# –––– Chat / Playerlist ––––
		self.cplbox = gtk.HBox()
		self.vpan.add2(self.cplbox)
		
		# ———— Chat ————
		self.chat = ChatWidget()
		self.chat.send_btn.connect('clicked', self.send_message)
		self.chat.msg_entry.connect('activate', self.send_message)
		self.cplbox.pack_end(self.chat, expand=True, fill=True)

		# ———— Playerlist ————
		self.playerlist = PlayerlistWidget()
		self.cplbox.pack_start(self.playerlist, expand=False, fill=False)

		# ———— Events ————
		self.menu_bar.about.connect('activate', self.ev_about)
		self.menu_bar.game_leave.connect('activate', self.ev_leave)
		self.menu_bar.game_stop.connect('activate', self.ev_stop)
		self.menu_bar.game_start.connect('activate', self.ev_start)
		self.menu_bar.view_chat.connect('activate', self.ev_toggle_chat)
		self.menu_bar.view_playerlist.connect('activate', self.ev_toggle_playerlist)
		self.connect('destroy', self.ev_leave)
