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

from gi.repository import Gtk, Gio, Adw, GObject

from .model import Constants, Light, Group, Bridge, AuthenticationHandler, MyClass
from .invenctory import BridgeInvenctory, LightsInvenctory, GroupsInvenctory
from .widgets import LightActionRow, GroupActionRow, BridgeActionRow, LightPage, RoomPage

@Gtk.Template(resource_path='/org/gnome/House/window.ui')
class House(Adw.ApplicationWindow):
    __gtype_name__ = 'House'

    #APP variables
    signalHand = MyClass()

    #GTK variables
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
        self.update_bridges()
        self.init_leaflet()
        user_name = self.settings.get_string('hue-hub-user-name')
        self.signalHand.connect("light_selected_signal", self.test_callback)
        if user_name != None and user_name != '':
            self.update_lights()
            self.update_rooms()

    def test_callback(self, inst, obj):
        print("borcodio")
        if isinstance(obj, Light):
            light_page = LightPage(obj)
            self.lafleat_page_two.remove(self.lafleat_page_two.get_last_child())
            self.lafleat_page_two.append(light_page)
            self.leaflet.navigate(Adw.NavigationDirection.FORWARD)
        elif isinstance(obj, Group):
            group_page = RoomPage(obj)
            self.lafleat_page_two.remove(self.lafleat_page_two.get_last_child())
            self.lafleat_page_two.append(group_page)
            self.leaflet.navigate(Adw.NavigationDirection.FORWARD)

    def init_leaflet(self):
        auth = AuthenticationHandler(self.settings.get_string('hue-hub-user-name'))
        bridge = Bridge(self.settings.get_string('hue-hub-id'), self.settings.get_string('hue-hub-ip-address'))
        lights = LightsInvenctory.get_lights(bridge, auth)
        for light in lights:
            light_page = LightPage(light)
            self.lafleat_page_two.append(light_page)
            break

    def update_lights(self):
        auth = AuthenticationHandler(self.settings.get_string('hue-hub-user-name'))
        bridge = Bridge(self.settings.get_string('hue-hub-id'), self.settings.get_string('hue-hub-ip-address'))
        lights = LightsInvenctory.get_lights(bridge, auth)
        for light in lights:
            light_row_1 = LightActionRow(light, self.signalHand)
            self.lights_list_box.append(light_row_1)

    def update_rooms(self):
        auth = AuthenticationHandler(self.settings.get_string('hue-hub-user-name'))
        bridge = Bridge(self.settings.get_string('hue-hub-id'), self.settings.get_string('hue-hub-ip-address'))
        groups = GroupsInvenctory.get_groups(bridge, auth)
        for group in groups:
            group_row_1 = GroupActionRow(group, self.signalHand)
            self.rooms_list_box.append(group_row_1)

    def update_bridges(self):
        for bridge in BridgeInvenctory.get_bridges():
            bridge_row = BridgeActionRow(self.settings, self.bridge_toast_overlay, bridge)
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





