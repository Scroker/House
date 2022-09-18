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
from .widgets import LightActionRow, GroupActionRow, BridgeActionRow, LightPage

@Gtk.Template(resource_path='/org/gnome/House/window.ui')
class House(Adw.ApplicationWindow):
    __gtype_name__ = 'House'
    leaflet = Gtk.Template.Child()
    lafleat_page_two = Gtk.Template.Child()
    settings = Gio.Settings.new('org.gnome.House')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        light_page = LightPage()
        self.lafleat_page_two.append(light_page)
        self.leaflet.navigate(Adw.NavigationDirection.FORWARD)

    #@Gtk.Template.Callback()
    def on_leaflet_back(self, widget):
        print("Leaflet Back")

    #@Gtk.Template.Callback()
    def on_switch_activate(self, widget):
        print("Switch Activate")
