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

import threading
import xmlrpclib
import gettext
import time
import sys

t = gettext.translation("catchx", "locale")
_ = t.ugettext

class connector(dict):
	def __init__(self, server, port, ui):
		self.ui = ui
		self.server = xmlrpclib.ServerProxy('http://{0}:{1}'.format(server, port))

	def login(self, game, nick):
		self.session = self.cmd("login", (game, nick))
		self.started = False

		# –––– S→C Commands ––––
	def scc_started(self, par):
		self.ui.chat_update(_("* {0} started the game").format(par[0]))
		self.started = True

	def scc_chat(self, par):
		if '/me ' in par[1]:
			self.ui.chat_update("* {0} {1}".format(par[0], par[1][4:]))
		else:
			self.ui.chat_update("{0}: {1}".format(par[0], par[1]))

	def scc_pmove(self, par):
		self.ui.map.map_layout.remove(self.ui.map.figure)
		self.ui.map.map_layout.put(self.ui.map.figure, int(round(par[1] - 16,0)), int(round(par[2] - 45, 0)))
				
	def scc_joined(self, par):
		self.ui.chat_update(_("* {0} entered the room").format(par[0]))
		
	def scc_left(self, par):
		self.ui.chat_update(_("* {0} left the room").format(par[0]))
		
	def scc_color_assoc(self, par):
		self.color_assoc = par
		for player in par:
			if player[0] == 'misterx':
				self.ui.chat_update(_("* {0} is the Mister X!").format(player[1]))
			else:
				self.ui.chat_update(_("* {0} is the {1} player!").format(player[1], player[0]))

	# –––– Command → Function assoc ––––
	commands = {
		'started': scc_started,
		'chat': scc_chat,
		'pmove': scc_pmove,
		'joined': scc_joined,
		'left': scc_left,
		'color_assoc': scc_color_assoc,
	}

	def handle_messages(self):
		green = "\x1b\x5b1;32;40m"
		normal = "\x1b\x5b0;37;40m"
		while self.session:
			cmd, par = self.server.poll_message(self.session)

			if len(par) > 0 and not isinstance(par[0], str):
				par = par[0]

			if not cmd == None:
				print "{0}Broadcast: {1}{2}{3}".format(green,cmd,par,normal)

			if cmd in self.commands:
				self.commands[cmd](self, par)
				
			time.sleep(0.5)

	def run(self):
		self.msg_thread = threading.Thread(target=self.handle_messages)
		self.msg_thread.start()

	def cmd(self, command, params=()):
		red = "\x1b\x5b1;31;40m"
		normal = "\x1b\x5b0;37;40m"

		print "{0}To server: {1}{2}{3}".format(red,command,params,normal)
		try:
			answer = getattr(self.server,command)(*params)
		except xmlrpclib.Fault:
			print _("Server fault:")
			raise
			sys.exit(0)
		if answer != None:
			print "\t→ {0}".format(answer)
		return answer

	#def __getitem__(self, key):
    #	#try:
	#	print key
	#	return dict.__getitem__(self, key)
	#	#except KeyError:
    #	#	return getattr(self.server,key)(*params)
