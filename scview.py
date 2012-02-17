#!/usr/bin/python2

# SCView - Security Camera Viewer
# Provides a simple interface to view multiple URI paths
# Written by: Jason Gardner
# https://github.com/Buhrietoe/scview

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygtk, gtk, gobject
import pygst
pygst.require('0.10')
import gst

class GTK_Main:
  
  def __init__(self):
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_title('SCView')
    window.set_default_size(640, 480)
    window.connect('destroy', gtk.main_quit, 'WM destroy')
    self.movie_window = gtk.DrawingArea()
    window.add(self.movie_window)
    window.show_all()
    
    self.player = gst.parse_launch('rtspsrc name=source ! decodebin !autovideosink')
    self.source = self.player.get_by_name('source')
    bus = self.player.get_bus()
    bus.add_signal_watch()
    bus.enable_sync_message_emission()
    bus.connect('message', self.on_message)
    bus.connect('sync-message::element', self.on_sync_message)

    self.source.props.location = 'rtsp://admin:admin@10.0.0.105/CH002.sdp'
    self.player.set_state(gst.STATE_PLAYING)
    
  def on_message(self, bus, message):
    t = message.type
    if t == gst.MESSAGE_EOS:
      self.player.set_state(gst.STATE_NULL)
    elif t == gst.MESSAGE_ERROR:
      self.player.set_state(gst.STATE_NULL)
      err, debug = message.parse_error()
      print 'Error: %s' % err, debug
  
  def on_sync_message(self, bus, message):
    if message.structure is None:
      return
    message_name = message.structure.get_name()
    if message_name == 'prepare-xwindow-id':
      imagesink = message.src
      imagesink.set_property('force-aspect-ratio', True)
      gtk.gdk.threads_enter()
      imagesink.set_xwindow_id(self.movie_window.window.xid)
      gtk.gdk.threads_leave()
      
GTK_Main()
gtk.gdk.threads_init()
gtk.main()
