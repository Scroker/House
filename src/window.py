# window.py
#
# Copyright 2021 Giorgio Dramis
#
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
import gi
import socket
import platform

from gi.repository import Gtk, Gio, Adw

@Gtk.Template(resource_path='/org/gnome/House/window.ui')
class House(Adw.ApplicationWindow):
    __gtype_name__ = 'House'

    settings = Gio.Settings.new('org.gnome.House')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

