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

__import__("pygtk").require('2.0')
import gtk
import sys
import locale
import gettext
import os
from optparse import OptionParser
from modules import ui as ui
from modules import uilogin as uilogin
from modules import connector as connector
APP_NAME = 'CatchX' # Just if we have to change the name for somewhat reason
APP_VER = 0.15

gtk.gdk.threads_init()

if __name__ == '__main__':
	
	
	parser = OptionParser()
	parser.add_option("-c", "--config", dest="config_file", default="{0}/.catchx.conf".format(os.getenv('USERPROFILE') or os.getenv('HOME')),
					  help="use CONFIG as config-file", metavar="CONFIG")
	parser.add_option("-l", "--skip-login-dialog",
					  action="store_false", dest="show_login_dialog", default=True,
					  help="skip login dialog")
	parser.add_option("-m", "--create-room",
					  action="store_true", dest="login_createroom", default=False,
					  help="create new room")
	parser.add_option("-r", "--room", dest="login_room", default=None,
					  help="join/create room ROOM", metavar="ROOM")
	parser.add_option("-n", "--nick", dest="login_nick", default="Anonymous",
					  help="use NICK as nick for this session", metavar="NAME")
	parser.add_option("-s", "--server", dest="login_server", default="master.catchx.net",
					  help="connect with server SERVER", metavar="SERVER")
	parser.add_option("-p", "--port", dest="login_port", default=20211,
					  help="connect with server on port PORT", type="int", metavar="PORT")
	(options, args) = parser.parse_args()
	
	server = None
	session = None
	
	#translation

	gettext.bindtextdomain('catchx', 'locale')
	gettext.textdomain('catchx')
	_ = gettext.gettext

	print _('Starting {0} v{1}').format(APP_NAME, APP_VER)

	game_win = ui.GameWindow()
	game_win.maximize()
	game_win.show_all()
	game_win.set_icon_from_file("img/logo.png")
	game_win.set_title(_("CatchX"))

	connection = connector.connector(options.login_server, options.login_port, game_win)
	login = uilogin.LoginDialog(connection)
	login.set_icon_from_file("img/logo.png")
	login.set_title(_("{0} Login".format(APP_NAME)))
		
	#if options.show_login_dialog:
	resp = login.run()
	if not resp: sys.exit(0)
	#else:
	#	if not ( options.login_room and options.login_nick):
	#		print "Cannot skip login dialog!"
	#		resp = login.run()
	#		if not resp: sys.exit(0)
	#	else:
	#		resp = 100
	login.hide()

	
	if resp == 200:
		connection.cmd("create_game", (login.game_entry.get_text(),
				login.description_entry.get_text()))
		game = login.game_entry.get_text()
	elif resp == 100:
		for button in login.buttons:
			if button.get_active():
				game = login.buttons[button]
	
	connection.login(game, options.login_nick)
	game_win.logged_in(connection)
	
	try:
		gtk.main()
	except KeyboardInterrupt:
		game_win.ev_leave(None)
		
