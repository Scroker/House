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
from .model import Constants, PhilipsHueListener
from .widgets import LightActionRow, GroupActionRow, BridgeActionRow, LightPage

@Gtk.Template(resource_path='/org/gnome/House/window.ui')
class House(Adw.ApplicationWindow):
    __gtype_name__ = 'House'
    leaflet = Gtk.Template.Child()
    bridge_toast_overlay = Gtk.Template.Child()
    lafleat_page_two = Gtk.Template.Child()
    info_menu_button = Gtk.Template.Child()
    bridges_list_box = Gtk.Template.Child()
    rooms_list_box = Gtk.Template.Child()
    lights_list_box = Gtk.Template.Child()
    settings = Gio.Settings.new('org.gnome.House')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_css()
        self.init_leaflet()
        self.update_lights()
        self.update_rooms()
        self.update_bridges()
        print(socket.gethostname())

    def init_leaflet(self):
        light_page = LightPage(None)
        self.lafleat_page_two.append(light_page)
        self.leaflet.navigate(Adw.NavigationDirection.FORWARD)

    def update_lights(self):
        light_row_1 = LightActionRow()
        self.lights_list_box.append(light_row_1)
        light_row_2 = LightActionRow()
        self.lights_list_box.append(light_row_2)
        light_row_3 = LightActionRow()
        self.lights_list_box.append(light_row_3)

    def update_rooms(self):
        room_row = GroupActionRow()
        self.rooms_list_box.append(room_row)

    def update_bridges(self):
        listener = PhilipsHueListener()
        if listener.info != None :
            bridge = listener.get_bridge()
            bridge_row = BridgeActionRow(self, self.bridge_toast_overlay, bridge)
            self.bridges_list_box.append(bridge_row)

    def load_css(self):
        css_provider = Gtk.CssProvider()
        try:
            css_provider.load_from_resource(resource_path=Constants.APPLICATION_STYLE)
        except GLib.Error as e:
            print(f"Error loading CSS : {e} ")
            return None
        return css_provider

    #@Gtk.Template.Callback()
    def on_leaflet_forward(self, widget):
        if self.page2_leaflet.get_folded():
            self.page2_leaflet.navigate(Adw.NavigationDirection.FORWARD)

    @Gtk.Template.Callback()
    def on_leaflet_back(self, widget):
        if self.leaflet.get_folded():
            self.leaflet.navigate(Adw.NavigationDirection.BACK)


