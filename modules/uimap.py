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

import gtk
import locale
import gettext

#######################################
#### Needed: Cleanup of this file. ####
#######################################

t = gettext.translation("catchx", "locale")
_ = t.ugettext
class MapWidget(gtk.Table):
	def img_size(self, img):
		pixbuf = img.get_pixbuf()
		return pixbuf.get_width(), pixbuf.get_height()

	def move_figure(self, button):
		self.map_layout.remove(self.lay)
		self.map_layout.put(self.lay, -100, -100)
		self.map_layout.remove(self.buttonbox)
		self.map_layout.put(self.buttonbox, -100, -100)
		self.tself.connection.cmd("pmove", (self.tself.connection.session, int(round(self.lastclick['x'],0)), int(round(self.lastclick['y'],0)))) #yeah! self.tself.!  super() kinda sucks
		
	def map_click(self, eventbox, button):
		if not self.tself.connection.started:
			return False
	#	if not button.x >= punkt -10 and button.y >= punkt-10 and button.x <= punkt +10 and button.y <= punkt-10:
		self.map_layout.remove(self.lay)
		self.map_layout.put(self.lay, button.x - 11.5, button.y - 14)
		self.map_layout.remove(self.buttonbox)
		self.map_layout.put(self.buttonbox, button.x, button.y + 20)
		
		self.lastclick = {'x' : button.x, 'y' : button.y}
	
	def __init__(self, filename, tself):
		self.tself = tself
		gtk.Table.__init__(self, 2, 2)
		#gtk.HBox.__init__(self)
		
		self.event_box = gtk.EventBox()
		self.attach(self.event_box, 0, 1, 0, 1)
		
		self.map_layout = gtk.Layout()
		self.event_box.add(self.map_layout)
		#self.pack_start(self.map_layout, expand=True, fill=True)
		
		self.copyright = gtk.Label(_("Map © 2005 André Flöter"))

		# ———— Weißer hintergrund ————
		color = gtk.gdk.color_parse('#FFFFFF')
		self.map_layout.modify_bg(gtk.STATE_NORMAL, color)

		# ———— Scrollbars ————
		v_adj = self.map_layout.get_vadjustment()
		v_adj.step_increment = 10
		self.v_scroll = gtk.VScrollbar(v_adj)
		self.attach(self.v_scroll, 1, 2, 0, 1, 0, gtk.EXPAND|gtk.FILL)
		#self.pack_start(self.v_scroll, expand=False, fill=False)

		h_adj = self.map_layout.get_hadjustment()
		h_adj.step_increment = 10
		self.h_scroll = gtk.HScrollbar(h_adj)
		self.attach(self.h_scroll, 0, 1, 1, 2, gtk.EXPAND|gtk.FILL, 0)		
		#self.pack_start(self.h_scroll, expand=False, fill=False)

		self.map_pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
		self.map_image = gtk.image_new_from_pixbuf(self.map_pixbuf)
		
		img_size = self.img_size(self.map_image)
		self.map_layout.set_size(*img_size)
		self.map_layout.put(self.map_image, 0, 0)
		self.map_layout.put(self.copyright, 0, 0)
				
                               
		FIGURES = ('blue','green','misterx','red','white','yellow')
		x,y = 0, 0
		for c in FIGURES:
			x += 30
			y += 30
			self.figure = gtk.Image()	
			self.figure.set_from_file("img/figures/{0}.png".format(c))
			self.map_layout.put(self.figure, x, y)

		self.lay = gtk.Image()	
		self.lay.set_from_file("img/overlay.png")
		self.map_layout.put(self.lay, -100, -100) #invisible

		self.buttonbox = gtk.HBox()
		
		self.movebtn_bus = gtk.Button(_("Bus"))
		#btn.set_sensitive(False)
		self.movebtn_bus.connect("clicked", self.move_figure)
		self.buttonbox.add(self.movebtn_bus)
		
		self.movebtn_tram = gtk.Button(_("Tram"))
		#self.movebtn_tram.set_sensitive(False)
		self.movebtn_tram.connect("clicked", self.move_figure)
		self.buttonbox.add(self.movebtn_tram)
		
		self.movebtn_taxi = gtk.Button(_("Taxi"))
		#self.movebtn_taxi.set_sensitive(False)
		self.movebtn_taxi.connect("clicked", self.move_figure)
		self.buttonbox.add(self.movebtn_taxi)
		
		self.movebtn_ship = gtk.Button(_("Ship"))
		#self.movebtn_ship.set_sensitive(False)
		self.movebtn_ship.connect("clicked", self.move_figure)
		self.buttonbox.add(self.movebtn_ship)
		
		self.map_layout.put(self.buttonbox, -100, -100) #invisible
		
		self.event_box.connect("button_press_event", self.map_click)
