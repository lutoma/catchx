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
import gettext

t = gettext.translation("catchx", "locale")
_ = t.ugettext

class LoginDialog(gtk.Dialog):

	def __init__(self, connection):
		gtk.Dialog.__init__(self)
		
		# ——— Logo ———	
		image = gtk.Image()
		image.set_from_file("img/logo.png")
		self.vbox.pack_start(image, padding=5)
		image.show()
		
		separator = gtk.HSeparator()
		self.vbox.pack_start(separator)
		separator.show()

		## Normal List ##
		self.buttonbox  = gtk.VBox()
		self.vbox.pack_start(self.buttonbox)

		self.buttons = {}
		#games = (['ABC', 'Open for everyone', 'Lutoma', ('Lutoma', 'vIiRuS', 'Pixelmann'), False], ['Cba', 'Our private game', 'Lutoma', ('Lutoma', 'vIiRuS', 'Pixelmann'), True])
		games = connection.cmd("get_gamelist")
		if not games == None:
			for game in games:
				try:
					button = gtk.RadioButton(button)
				except UnboundLocalError:
					button = gtk.RadioButton()
				if game[4]:
					button.set_sensitive(False)
					
				box = gtk.VBox()
				button.add(box)
				label = gtk.Label()
				game[3] = ', '.join(game[3])
				game[4] = _("Yes") if game[4] else _("No")
				label.set_markup(_("<big>{0}</big> - '{1}'\n<small>Creator: {2}\nPlayers: {3}\nRunning: {4}</small>").format(*game))

				box.pack_end(label, fill=True, expand=True)
				
				self.buttonbox.pack_end(button, fill=True, expand=True)
				self.buttons[button] = game[0]
		else:
			label = gtk.Label()
			label.set_markup(_("<big>No active rooms found.</big>"))
			self.buttonbox.pack_end(label, fill=True, expand=True, padding=10)

		self.buttonbox.show_all()
		
		
		## Advanced ##
		
		# ——— Table ———	
		self.nrtable = gtk.Table(rows=3, columns=3)
		self.vbox.pack_start(self.nrtable, padding=5)
		self.nrtable.hide()
		self.nrtable.set_col_spacings(5)
		self.nrtable.set_row_spacings(5)
		
		# ——— Game ———
		label = gtk.Label(_('Name:'))
		self.nrtable.attach(label, 0, 1, 0, 1)

		self.game_entry = gtk.Entry()
		self.nrtable.attach(self.game_entry, 1, 2, 0, 1)
		

		# ———— Nickname ————
		label = gtk.Label(_('Description:'))
		self.nrtable.attach(label, 0, 1, 1, 2)

		self.description_entry = gtk.Entry()
		self.nrtable.attach(self.description_entry, 1, 2, 1, 2)

		# ——— Buttons ———
		def shownewroom(widget):
			self.buttonbox.hide()
			self.nrtable.show_all()
			new_room_button.hide()
			self.add_button(_('Create'), 200).grab_default() #STOCK_GO_FORWARD

		reload_button = gtk.Button(_('Reload list'))
		self.action_area.pack_end(reload_button)
		#advanced_button.connect("clicked", showadvanced)	

		new_room_button = gtk.Button(_('Create new room'))
		self.action_area.pack_end(new_room_button)
		new_room_button.connect("clicked", shownewroom)

		self.add_button(_('Connect'), 100).grab_default() #STOCK_GO_FORWARD
		
		self.set_border_width(5)

		self.action_area.show_all()
