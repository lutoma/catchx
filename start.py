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
import gtk
import ui
import sys
import xmlrpclib
import locale
import gettext

APP_NAME = 'CatchX' # Just if we have to change the name for somewhat reason
APP_VER = 0.15

gtk.gdk.threads_init()

if __name__ == '__main__':
	
	server = None
	session = None
	
	#translation
	t = gettext.translation("catchx", "locale")
	_ = t.ugettext
	print _('Starting {0} v{1}').format(APP_NAME, APP_VER)

	game_win = ui.GameWindow()
	game_win.maximize()
	game_win.show_all()
	game_win.set_icon_from_file("img/logo.png")
	game_win.set_title(_("CatchX"))
	
	login = ui.LoginDialog()
	login.show_all() #REMOVE THIS LATER!
	login.set_icon_from_file("img/logo.png")
	login.set_title(_("CatchX Login"))
	resp = login.run()
	if not resp: sys.exit(0)
	login.hide()
	
	try:
		server = login.server_entry.get_text()
		port = login.port_entry.get_text()
	except:
		server = 'master.catchx.net'
		port = 20211
		
	server = xmlrpclib.ServerProxy('http://{0}:{1}'.format(
		server, port))

	if resp == 100:
		if login.create_btn.get_active():
			server.create_game(login.game_entry.get_text(),
				login.password_entry.get_text())
	
		session = server.login(login.game_entry.get_text(),
			login.password_entry.get_text(), login.nick_entry.get_text())

		game_win.logged_in(server, session)
			
		gtk.main()
