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

gi.require_version('Handy', '1')

from gi.repository import Gtk, Gio, Handy
from .rest_utilities import RESTUtilities
from .model import Bridge
from .model import AuthenticationHandler
from .group_view import GroupViewPreferenceGroup
from .light_view import LightExpanderRow

@Gtk.Template(resource_path='/org/scroker/LightController/window.ui')
class LightcontrollerWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'LightcontrollerWindow'

    Handy.init()
    squeezer = Gtk.Template.Child()
    headerbar_switcher = Gtk.Template.Child()
    bottom_switcher = Gtk.Template.Child()
    bridge_preference_page = Gtk.Template.Child()
    groups_preferences_page = Gtk.Template.Child()
    lights_preference_page = Gtk.Template.Child()
    connect_button = Gtk.Template.Child()
    press_button_label = Gtk.Template.Child()
    rest_utility = RESTUtilities()
    settings = Gio.Settings.new('org.scroker.LightController')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        bridge = Bridge(self.settings.get_string('hue-hub-id'), self.settings.get_string('hue-hub-ip-address'))
        auth_handler = AuthenticationHandler(self.settings.get_string('hue-hub-user-name'))
        self.connect_button.connect('clicked', self.on_connect_button, bridge)
        self.squeezer.connect("notify::visible-child",self.on_headerbar_squeezer_notify)
        try:
            self.update_stack_view(bridge, auth_handler)
        except Exception as error:
            self.connect_button.set_sensitive(True)
            self.connect_button.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

    # GtkSqueeze on notify visible child functions
    def on_headerbar_squeezer_notify(self, squeezer, event):
	    child = squeezer.get_visible_child()
	    self.bottom_switcher.set_reveal(child != self.headerbar_switcher)

    # GtkButton on click functions
    def on_connect_button(self, button, bridge):
        for bridge in self.rest_utility.discover_bridges():
            try:
                device_name = socket.gethostname() + "#" + platform.system()
                auth_handler = self.rest_utility.pair_with_the_bridge(bridge, device_name)
                self.update_stack_view(bridge, auth_handler)
                self.settings.set_string('hue-hub-id', bridge.bridge_id)
                self.settings.set_string('hue-hub-ip-address', bridge.internal_ip_address)
                self.settings.set_string('hue-hub-user-name', auth_handler.user_name)
                self.connect_button.set_sensitive(False)
                self.press_button_label.set_visible(False)
                break
            except Exception as error:
                if '\'type\': 101' in str(error) :
                    self.press_button_label.set_visible(True)

    # GtkStackView update functions
    def update_stack_view(self, bridge, auth_handler):
        config = self.rest_utility.get_config(bridge, auth_handler)
        self.update_bridge_stack_view(config)
        lights = self.rest_utility.get_lights(bridge, auth_handler)
        self.update_light_stack_view(lights, bridge, auth_handler)
        groups = self.rest_utility.get_groups(bridge, auth_handler)
        self.update_groups_stack_view(groups, bridge, auth_handler)

    def update_light_stack_view(self, lights, bridge, auth_handler):
        preference_group = Handy.PreferencesGroup()
        preference_group.set_title('Luci')
        for light_id in lights :
            row = LightExpanderRow(bridge, auth_handler, lights[light_id], light_id)
            preference_group.add(row)
        preference_group.show()
        self.lights_preference_page.add(preference_group)

    def update_groups_stack_view(self, groups, bridge, auth_handler):
        for index in groups:
            preference_group = GroupViewPreferenceGroup(bridge, auth_handler, groups[index], index)
            self.groups_preferences_page.add(preference_group)

    def update_bridge_stack_view(self, config):
        preference_group = Handy.PreferencesGroup()
        preference_group.set_title(config['name'])
        bridgeid_label = Gtk.Label()
        bridgeid_label.set_label(config['bridgeid'])
        bridgeid_label.show()
        bridgeid_row = Handy.ActionRow()
        bridgeid_row.set_title('Bridge ID')
        bridgeid_row.add(bridgeid_label)
        bridgeid_row.show()
        ipaddress_label = Gtk.Label()
        ipaddress_label.set_label(config['ipaddress'])
        ipaddress_label.show()
        ipaddress_row = Handy.ActionRow()
        ipaddress_row.set_title('Indirizzo IP')
        ipaddress_row.add(ipaddress_label)
        ipaddress_row.show()
        mac_label = Gtk.Label()
        mac_label.set_label(config['mac'])
        mac_label.show()
        mac_row = Handy.ActionRow()
        mac_row.set_title('Indirizzo MAC')
        mac_row.add(mac_label)
        mac_row.show()
        timezone_label = Gtk.Label()
        timezone_label.set_label(config['timezone'])
        timezone_label.show()
        timezone_row = Handy.ActionRow()
        timezone_row.set_title('Time Zone')
        timezone_row.add(timezone_label)
        timezone_row.show()
        whitelist_row = Handy.ExpanderRow()
        whitelist_row.set_title('White list')
        whitelist_row.show()
        for api_key in config['whitelist']:
            api_label = Gtk.Label()
            api_label.set_label(config['whitelist'][api_key]['last use date'])
            api_label.show()
            api_row = Handy.ActionRow()
            api_row.set_title(config['whitelist'][api_key]['name'])
            api_row.add(api_label)
            api_row.show()
            whitelist_row.add(api_row)
        preference_group.add(ipaddress_row)
        preference_group.add(mac_row)
        preference_group.add(bridgeid_row)
        preference_group.add(timezone_row)
        preference_group.add(whitelist_row)
        preference_group.show()
        self.bridge_preference_page.add(preference_group)


