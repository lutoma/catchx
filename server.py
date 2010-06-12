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

from SimpleXMLRPCServer import SimpleXMLRPCServer
from optparse import OptionParser

import uuid
from collections import deque
import random

class Player(object):
	
	def __init__(self, nick):
		self.msgqueue = deque()
		self.nick = nick
		
	def has_messages(self):
		return len(self.msgqueue) > 0
		
	def push_message(self, cmd, *par):
		self.msgqueue.appendleft((cmd, par))
		
	def pop_message(self):
		return self.msgqueue.pop()


class Game(object):
	
	def __init__(self, description):
		self.players = set()
		self.description = description
		self.running = False
		
	def add_player(self, player):
		self.players.add(player)	
		self.broadcast('joined', player.nick)	
		
	def del_player(self, player):
		self.players.remove(player)
		self.broadcast('left', player.nick)	
		
	def start(self, nick):
		self.running = True
		self.broadcast('started', nick)
		FIGURES = ['blue','green','red','white','yellow']
		players = []
		for i in self.players:
			players.append(i.nick)
		p_to_n = zip(players, self.players)
		random.shuffle(players)
		colors = ['misterx'] + random.sample(FIGURES, len(players)-1)
		assoc = zip(colors, players)
		for i in assoc:
			for j in p_to_n: #inefficency ftw... -.-
				print "forloop"
				print i
				print j
				if j[0] == i[0]:
					print "if"
					print j
					print i
		self.broadcast('color_assoc', assoc)
	
	def broadcast(self, cmd, *par):
		for p in self.players:
			p.push_message(cmd, *par)
			
	def chat(self, nick, msg):
		self.broadcast('chat', (nick, msg))
	
	def pmove(self, sid, x, y):
		self.broadcast('pmove', (sid, x, y))


class Session(object):

	def __init__(self, game, player):
		self.game = game
		self.player = player


class CatchXServer(object):

	def __init__(self):
		self.games = dict()
		self.sessions = dict()

	def ping(self):
		return 'pong'
	
	def create_game(self, gid, description):
		if gid in self.games: return None
		
		self.games[gid] = Game(description)	
		return gid
	
	def login(self, gid, nick):
		if not gid in self.games: return 'wrong!' 
		
		game = self.games[gid]
		
		if game.running: return 'running!'
		
		player = Player(nick)
		game.add_player(player)
		
		sid = str(uuid.uuid4())
		self.sessions[sid] = Session(game, player)
		
		return sid
			
	def get_playerlist(self, sid):
		players = []
		for i in self.sessions[sid].game.players:
			players.append(i.nick)
		return players

	def get_gamelist(self):
		games = []
		for session in self.sessions:
			game = session.game
			print game
			games.append(["Name", game.description, 'Someone', game.players, game.running])
		return games

	def poll_message(self, sid):
		if self.sessions[sid].player.has_messages(): 
			return self.sessions[sid].player.pop_message()	
		else: return None, ()
		
	def say(self, sid, msg):
		if msg == '0xSPAMANDEGG':
			msg = """
            ^__^
            (oo)\_______
            (__)\       )\\/\\ 
                ||----w |
                ||     ||"""
		self.sessions[sid].game.chat(self.sessions[sid].player.nick, msg)
	
	def pmove(self, sid, x, y):
		self.sessions[sid].game.pmove(sid, x, y)
	
	def start_game(self, sid):
		self.sessions[sid].game.start(self.sessions[sid].player.nick)
		
	def logout(self, sid):
		session = self.sessions[sid]
		session.game.del_player(session.player)
		del self.sessions[sid]
					
					
if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-p", "--port", dest="port", default=20211,
					  help="specifies port to listen on", type="int", metavar="PORT")
	(options, args) = parser.parse_args()
	
	server = SimpleXMLRPCServer(('', options.port), allow_none=True)
	server.register_introspection_functions()
	server.register_instance(CatchXServer())
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print "Interrupted!"
		exit()
