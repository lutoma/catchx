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
import threading
import time
import locale
import gettext

t = gettext.translation("catchx", "locale")
_ = t.ugettext
class AboutDialog(gtk.AboutDialog):
	
	def __init__(self):
		gtk.AboutDialog.__init__(self)
		self.set_name(_("CatchX"))
		self.set_copyright(_("© 2009 CatchX Team"))
		self.set_website(_("http://www.catchx.net"))
		self.set_license("""CatchX is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

CatchX is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSEs.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with CatchX.  If not, see <http://www.gnu.org/licenses/>.
""")
		self.set_comments(_("“Quick, before it's too late!”"))
		self.set_authors(((_("Main developers:")),("- Lutoma (Lukas Martini)"), (""), (_("Contributors:")),("- vIiRuS (Phillip Thelen)"), ("- Waldteufel (Benjamin Richter)")))
		#self.set_artists((("Pixelmännchen (Robin Eberhard)"),))
		self.set_logo(gtk.gdk.pixbuf_new_from_file("img/logo.png"))
		self.set_wrap_license(True)

class LoginDialog(gtk.Dialog):

	def __init__(self):
		gtk.Dialog.__init__(self)
		
		# ——— Logo ———	
		image = gtk.Image()
		image.set_from_file("img/logo.png")
		self.vbox.pack_start(image, padding=5)
		
		separator = gtk.HSeparator()
		self.vbox.pack_start(separator)
		
		# ——— Table ———	
		table = gtk.Table(rows=3, columns=3)
		self.vbox.pack_start(table, padding=5)
		table.set_col_spacings(5)
		table.set_row_spacings(5)
		
		# ——— Game ———
		label = gtk.Label(_('Room:'))
		table.attach(label, 0, 1, 0, 1)

		self.game_entry = gtk.Entry()
		table.attach(self.game_entry, 1, 2, 0, 1)
		
		# ——— Password ———
		label = gtk.Label(_('Password:'))
		table.attach(label, 2, 3, 0, 1)
						
		self.password_entry = gtk.Entry()
		self.password_entry.set_visibility(False)
		table.attach(self.password_entry, 3, 4, 0, 1)

		# ———— Nickname ————
		label = gtk.Label(_('Nickname:'))
		table.attach(label, 0, 1, 1, 2)

		self.nick_entry = gtk.Entry()
		table.attach(self.nick_entry, 1, 2, 1, 2)

		# ——— Create game ———
		self.create_btn = gtk.ToggleButton(_('Create room'))
		self.create_btn.set_mode(True)
		table.attach(self.create_btn, 3, 4, 1, 2)
		
		self.game_entry.grab_focus()
		
		# ——— Advanced Table ———
		table = gtk.Table(rows=1, columns=3)
		table.set_col_spacings(5)
		table.set_row_spacings(5)
		
		# ——— Server ———
		label = gtk.Label(_('Server:'))
		table.attach(label, 0, 1, 0, 1)
		
		self.server_entry = gtk.Entry()
		self.server_entry.set_text('master.catchx.net')
		table.attach(self.server_entry, 1, 2, 0, 1)		

		# ——— Port ———
		label = gtk.Label(_('Port:'))
		table.attach(label, 2, 3, 0, 1)

		self.port_entry = gtk.Entry()
		self.port_entry.set_text('20211')
		table.attach(self.port_entry, 3, 4, 0, 1)
		
		# ——— Buttons ———
		def showadvanced(widget):
			self.advanced = True
			self.vbox.pack_start(table, padding=5)
			table.show_all()
			self.action_area.remove(button)
		
		button = gtk.Button(_('Advanced')) #STOCK_YES
		self.action_area.pack_end(button)
		button.connect("clicked", showadvanced)
		
		self.add_button(_('Connect'), 100).grab_default() #STOCK_GO_FORWARD
		self.set_border_width(5)
		
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

	

class StartWidget(gtk.VBox):
	
	def __init__(self):
		gtk.VBox.__init__(self)
		
		image = gtk.Image()
		image.set_from_file("img/logo.png")
		self.add(image)
		
		info = gtk.Label(_("""To start the game, press Game -> Start game!\nBut wait for the other players first, when the game is started, no new players can join the room!"""))
		self.add(info)

class ChatWidget(gtk.VBox):

	def __init__(self):
		gtk.VBox.__init__(self)
		
		self.chat_box = gtk.TextView()
		self.chat_buffer = self.chat_box.get_buffer()
		self.chat_box.set_editable(False)
		self.chat_text = _("* Welcome to CatchX!")
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
		
		self.liststore = gtk.ListStore(str, 'gboolean')
		self.treeview = gtk.TreeView(self.liststore)
		self.tvcolumn1 = gtk.TreeViewColumn('Text Only')
		
		self.liststore.append(['Open a File', True])
		self.liststore.append(['New File', True])
		self.liststore.append(['Print File', False])
		self.treeview.append_column(self.tvcolumn1)
		self.cell1 = gtk.CellRendererText()
		#self.cell1.set_property('cell-background', 'pink')
		self.tvcolumn1.pack_start(self.cell1, True)
		#self.tvcolumn1.set_attributes(self.cell1, text=2,
        #                              cell_background_set=3)
	
		self.pack_start(self.treeview)

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
		game_menu.append(self.game_stop)
		
		self.game_leave = gtk.MenuItem(_('Leave CatchX'))
		game_menu.append(self.game_leave)
		
		#View-Menu
		view_menu = gtk.Menu()
		view_item = gtk.MenuItem(_('View'))
		view_item.set_submenu(view_menu)
		self.append(view_item)
		
		self.view_chat = gtk.MenuItem(_('Show Chat'))
		view_menu.append(self.view_chat)
		
		self.view_playerlist = gtk.MenuItem(_('Show Playerlist'))
		view_menu.append(self.view_playerlist)

		#MisterX-Menu
		misterx_menu = gtk.Menu()
		misterx_item = gtk.MenuItem(_('Mister X'))
		misterx_item.set_submenu(misterx_menu)
		self.append(misterx_item)
		
		self.misterx_bankrobbery = gtk.MenuItem(_('Bank robbery'))
		misterx_menu.append(self.misterx_bankrobbery)
		
		self.misterx_stheft = gtk.MenuItem(_('Simple theft'))
		misterx_menu.append(self.misterx_stheft)
		
		self.misterx_gtheft = gtk.MenuItem(_('Grand theft'))
		misterx_menu.append(self.misterx_gtheft)
		
		self.misterx_burglary = gtk.MenuItem(_('Burglary'))
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
		self.server.start_game(self.session)
		#self.actions.btn.set_sensitive(True)
		#self.vpan.add1(self.up_hpan)

	def ev_leave(self, ev):
		self.server.logout(self.session)
		self.session = None
		gtk.main_quit()

	def ev_stop(self, ev):
		self.server.stop_game(self.session)
		
	def chat_update(self, text):
		self.chat.chat_text += "\n" + text
		self.chat.chat_buffer.set_text(self.chat.chat_text)
		self.chat.chat_box.scroll_mark_onscreen(self.chat.chat_buffer.get_insert())


	def send_message(self, widget):
		self.server.say(self.session, self.chat.msg_entry.get_text())
		self.chat.msg_entry.set_text('')

	# –––– S→C Commands ––––
	def scc_started(self, par):
		self.chat_update(_("* {0} started the game").format(par))
		self.started = True

	def scc_chat(self, par):
		if '/me ' in par[1]:
			self.chat_update("* {0} {1}".format(par[0], par[1][4:]))
		else:
			self.chat_update("{0}: {1}".format(par[0], par[1]))

	def scc_pmove(self, par):
		self.map.map_layout.remove(self.map.figure)
		self.map.map_layout.put(self.map.figure, round(par[1] - 16,0), round(par[2] - 45, 0))
				
	def scc_joined(self, par):
		self.chat_update(_("* {0} entered the room").format(par))
		
	def scc_left(self, par):
		self.chat_update(_("* {0} left the room").format(par))
		
	def scc_color_assoc(self, par):
		for player in par: #why not par[0] ? → odd!
			if player[0] == 'misterx':
				self.chat_update(_("* {0} is the Mister X!").format(player[1]))
			else:
				self.chat_update(_("* {0} is the {1} player!").format(player[1], player[0]))

	# –––– Command → Function assoc ––––
	commands = {
		'started': scc_started,
		'chat': scc_chat,
		'pmove': scc_pmove,
		'joined': scc_joined,
		'left': scc_left,
		'color_assoc': scc_color_assoc,
		'test': print, #debug, 4 sure
	}

	def handle_messages(self):
		while self.session:
			cmd, par = self.server.poll_message(self.session)
			
			if len(par) > 0:
				par = par[0] #Kinda odd

			if cmd in commands:
				commands[cmd](par)
				
			time.sleep(0.5)

	def logged_in(self, server, session):
		self.server = server
		self.session = session
		self.started = False
		self.msg_thread.start()
	
	def __init__(self):
		gtk.Window.__init__(self)
		
		self.msg_thread = threading.Thread(target=self.handle_messages)

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
		
		# ———— Startinfo ————
		self.info = StartWidget()
		#self.vpan.add1(self.info)
		
		# ———— Set the right size for the chat/playerlist ————
		size = self.get_size()
		uppersize = 1300 #size returns incorrect values and this doesnt seem to do anything -.-
		print size[0]
		print size[1]
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
		self.cplbox.pack_end(self.chat, expand=True, fill=True)

		# ———— Playerlist ————
		self.playerlist = PlayerlistWidget()
		self.cplbox.pack_start(self.playerlist, expand=False, fill=False)

		# ———— Events ————
		self.menu_bar.about.connect('activate', self.ev_about)
		self.menu_bar.game_leave.connect('activate', self.ev_leave)
		self.menu_bar.game_stop.connect('activate', self.ev_stop)
		self.menu_bar.game_start.connect('activate', self.ev_start)
