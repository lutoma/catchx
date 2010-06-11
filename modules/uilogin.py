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
		
