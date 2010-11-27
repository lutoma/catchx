#!/usr/bin/env python
# -*- coding: utf8 -*-
#    This file is part of CatchX.
#
#    CatchX is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    CatchX is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with CatchX.  If not, see <http://www.gnu.org/licenses/>.

# Yay, this might get an price for the worst-commented code ever. But please don't blame us, we didn't think any other human might ever read this.
import logging
import os
from SimpleXMLRPCServer import SimpleXMLRPCServer
from optparse import OptionParser

from collections import deque
import random

class Player(object):
	
	def __init__(self, nick):
		self.msgqueue = deque()
		self.nick = nick
		self.color = None
		self.position = None
		
	def has_messages(self):
		return len(self.msgqueue) > 0
		
	def push_message(self, cmd, *par):
		self.msgqueue.appendleft((cmd, par))
		
	def pop_message(self):
		return self.msgqueue.pop()


class Game(object):

	def __init__(self, description):
		self.players = dict()
		self.description = description
		self.running = False
		
	def add_player(self, player):
		self.players[id(player)] = player
		self.broadcast('joined', (id(player),player.nick))	

	def del_player(self, pid):
		del self.players[pid]
		self.broadcast('left', (id(pid),))	
		
	def start(self, player):
		if self.running: return
		self.running = True
		self.broadcast('started', (id(player),))
		FIGURES = ['blue','green','red','white','yellow']
		players = []
		for i in self.players:
			players.append(i)
		#random.shuffle(players)
		colors = ['misterx'] + random.sample(FIGURES, len(players)-1)
		assoc = zip(players, colors)
		self.broadcast('color_assoc', assoc)
		for i in assoc:
			self.players[i[0]].color = i[1]

	def broadcast(self, cmd, *par):
		for p in self.players:
			self.players[p].push_message(cmd, *par)
			
	def chat(self, player, msg):
		self.broadcast('chat', (id(player), msg))
	
	def pmove(self, pid, x, y):
		if self.players[pid].color != "misterx":
			self.broadcast('pmove', (pid, x, y))

class CatchXServer(object):

	def __init__(self):
		self.games = dict()
		self.players = dict()

	def ping(self):
		return 'pong'
	
	def create_game(self, gid, description):
		if gid in self.games: return False
		self.games[gid] = Game(description)
		return True
	
	def login(self, gid, nick):
		game = self.games[gid]
		
		if game.running: return False
		
		player = Player(nick)
		game.add_player(player)
		player.game = game
		
		pid = id(player)
		self.players[pid] = player
		return pid
			
	def get_playerlist(self, pid):
		players = []
		for i in self.players[pid].game.players:
			players.append((id(self.players[i]), self.players[i].nick))
		return players

	def get_gamelist(self):
		games = []
		for gameName in self.games:
			game = self.games[gameName]
			players= []
			for player in game.players:
				players.append(game.players[player].nick)
			games.append([gameName, game.description, 'Someone', players, game.running])
		try:
			return games
		except:
			return []

	def poll_message(self, pid):
		if self.players[pid].has_messages(): 
			return self.players[pid].pop_message()
		else: return None, ()

	def say(self, pid, msg):
		self.players[pid].game.chat(self.players[pid], msg)
	
	def pmove(self, pid, x, y):
		self.players[pid].game.pmove(pid, x, y)
	
	def start_game(self, pid):
		self.players[pid].game.start(self.players[pid])
		
	def logout(self, pid):
		player = self.players[pid]
		player.game.del_player(pid)
		if(len(player.game.players) == 0):
			del self.games[dict([(v, k) for (k, v) in self.games.iteritems()])[player.game]]
		del self.players[pid]


def daemonize(pidfile):
	log.info('Daemonizing')
	try:
		pid = os.fork()
	except OSError, e:
		log.exception('Couldn\'t fork!')
		raise Exception, "%s [%d]" % (e.strerror, e.errno)

	if (pid != 0):
		logging.info('Forked with PID {0}'.format(pid))
		f = open(pidfile, 'w')
		f.write(str(pid) + '\n')
		f.close()
		os._exit(0)

if __name__ == "__main__":
	logging.basicConfig()
	log = logging.getLogger("catchxd")

	parser = OptionParser()
        parser.add_option("-a", "--address", dest="address", default="0.0.0.0",
                                          help="Address to bind to", metavar="ADDRESS")
	parser.add_option("-p", "--port", dest="port", default=20211,
					  help="specifies port to listen on", type="int", metavar="PORT")
	parser.add_option("-d", "--daemon", action="store_true", dest="daemon", default=False,
					  help="run as daemon")
	parser.add_option("-D", "--debug", action="store_true", dest="debug", default=False,
					  help="run in debug mode")
	parser.add_option("-q", "--quiet", action="store_true", dest="quiet", default=False,
					  help="run silently")
        parser.add_option("-P", "--file", dest="pidfile", default="/var/run/catchx.pid",
                                          help="Where to save PID", metavar="FILE")

	(options, args) = parser.parse_args()

	if options.debug:
		log.setLevel(logging.DEBUG)
	elif not options.quiet:
		log.setLevel(logging.INFO)

	log.info('Starting catchxd')
	if options.daemon:
		daemonize(options.pidfile)
	
	server = SimpleXMLRPCServer((options.address, options.port), allow_none=True)
	server.register_introspection_functions()
	server.register_instance(CatchXServer())
	
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print "Interrupted!"
		exit()
