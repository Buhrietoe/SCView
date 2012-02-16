#!/usr/bin/python

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

from gi.repository import Gtk

class MainWindow(Gtk.Window):

  def __init__(self):
    Gtk.Window.__init__(self, title="SCView")

w = MainWindow()
w.connect('delete-event', Gtk.main_quit)
w.show_all()
Gtk.main()
