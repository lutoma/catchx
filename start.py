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
from optparse import OptionParser

APP_NAME = 'CatchX' # Just if we have to change the name for somewhat reason
APP_VER = 0.15

gtk.gdk.threads_init()

if __name__ == '__main__':
	
	
	parser = OptionParser()
	parser.add_option("-l", "--skip-login-dialog",
					  action="store_false", dest="show_login_dialog", default=True,
					  help="skip login dialog")
	parser.add_option("-c", "--create-room",
					  action="store_true", dest="login_createroom", default=False,
					  help="create new room")
	parser.add_option("-r", "--room", dest="login_room", default=None,
					  help="join/create room ROOM", metavar="ROOM")
	parser.add_option("-u", "--nick", dest="login_nick", default=None,
					  help="set nick to NICK", metavar="NAME")
	parser.add_option("-k", "--password", dest="login_pw", default=None,
					  help="use room password PASSWORD", metavar="PASSWORD")
	parser.add_option("-s", "--server", dest="login_server", default="master.catchx.net",
					  help="connect with server SERVER", metavar="SERVER")
	parser.add_option("-p", "--port", dest="login_port", default=20211,
					  help="connect with server on port PORT", type="int", metavar="PORT")
	(options, args) = parser.parse_args()
	
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
	
	# set the fields contents on their values submitted from the commandline or to the defaults
	login.create_btn.set_active(options.login_createroom)
	login.server_entry.set_text(options.login_server)
	login.port_entry.set_text(str(options.login_port))
	if options.login_room:
		login.game_entry.set_text(options.login_room)
	if options.login_room:
		login.game_entry.set_text(options.login_room)
	if options.login_nick:
		login.nick_entry.set_text(options.login_nick)
	if options.login_pw:
		login.password_entry.set_text(options.login_pw)
		
	if options.show_login_dialog:
		resp = login.run()
		if not resp: sys.exit(0)
	else:
		if not ( options.login_room and options.login_nick and options.login_pw ):
			print "Cannot skip login dialog!"
			resp = login.run()
			if not resp: sys.exit(0)
		else:
			resp = 100
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
