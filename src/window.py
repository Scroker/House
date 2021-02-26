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

gi.require_version('Handy', '1')

from gi.repository import Gtk, Gio, Handy
from .bridge_utilities import BrigdeUtilities

@Gtk.Template(resource_path='/org/scroker/LightController/window.ui')
class LightcontrollerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'LightcontrollerWindow'

    Handy.init()
    squeezer = Gtk.Template.Child()
    headerbar_switcher = Gtk.Template.Child()
    bottom_switcher = Gtk.Template.Child()
    press_button_label = Gtk.Template.Child()
    bridge_info_preference_group = Gtk.Template.Child()
    groups_preferences_page = Gtk.Template.Child()
    lights_preference_group = Gtk.Template.Child()
    connect_button = Gtk.Template.Child()
    utility = BrigdeUtilities()
    settings = Gio.Settings.new('org.scroker.LightController')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.squeezer.connect("notify::visible-child",self.on_headerbar_squeezer_notify)
        for bridge in self.utility.discover_bridges():
            self.connect_button.connect('clicked', self.on_connect_button, bridge)
            device_id = self.settings.get_string('device-id')
            try:
                config = self.utility.get_config(bridge, device_id)
                self.update_bridge_stack_view(config)
                lights = self.utility.get_lights(bridge, device_id)
                self.update_light_stack_view(lights, bridge, device_id)
                groups = self.utility.get_groups(bridge, device_id)
                self.update_groups_stack_view(groups, bridge, device_id)
            except Exception as error:
                self.connect_button.set_sensitive(True)
                self.connect_button.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

    def on_headerbar_squeezer_notify(self, squeezer, event):
	    child = squeezer.get_visible_child()
	    self.bottom_switcher.set_reveal(child != self.headerbar_switcher)

    def on_light_scale_moved(self, widget, bridge, device_id, index):
        self.utility.set_light_brightness(bridge, device_id, index, int(widget.get_value()))

    def on_light_switch_activated(self, widget, event, bridge, device_id, index, brightness_scale):
        if widget.get_active():
            self.utility.set_light_status(bridge, device_id, index, True)
            brightness_scale.set_sensitive(True)
        else :
            self.utility.set_light_status(bridge, device_id, index, False)
            brightness_scale.set_sensitive(False)

    def on_groups_switch_activated(self, widget, event, bridge, device_id, index):
        if widget.get_active():
            self.utility.set_group_action(bridge, device_id, index, True)
        else :
            self.utility.set_group_action(bridge, device_id, index, False)

    def on_connect_button(self, button, bridge):
        try:
            device_id = self.utility.pair_with_the_bridge(bridge)
            self.settings.set_string('device-id', device_id)
            config = self.utility.get_config(bridge, device_id)
            self.update_bridge_stack_view(config)
            lights = self.utility.get_lights(bridge, device_id)
            self.update_light_stack_view(lights, bridge, device_id)
            self.connect_button.set_sensitive(False)
            self.press_button_label.set_visible(False)
        except Exception as error:
            self.press_button_label.set_visible(True)

    def update_light_stack_view(self, lights, bridge, device_id):
        for index in lights :
            brightness_ad = Gtk.Adjustment(lights[index]['state']['bri'], 0, 254, 5, 10, 0)
            brightness_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=brightness_ad)
            brightness_scale.connect("value-changed", self.on_light_scale_moved, bridge, device_id, index)
            brightness_scale.set_valign(Gtk.Align.START)
            brightness_scale.set_digits(False)
            brightness_scale.set_hexpand(True)
            brightness_scale.set_sensitive(lights[index]['state']['on'])
            brightness_scale.show()
            switch = Gtk.Switch()
            switch.set_active(lights[index]['state']['on'])
            switch.connect("notify::active", self.on_light_switch_activated, bridge, device_id, index, brightness_scale)
            switch.set_valign(Gtk.Align.CENTER)
            switch.show()
            status_row = Handy.ActionRow()
            status_row.set_title('Accesa')
            status_row.add(switch)
            status_row.show()
            brightness_row = Handy.ActionRow()
            brightness_row.set_title('Luminosità')
            brightness_row.add(brightness_scale)
            brightness_row.show()
            row = Handy.ExpanderRow()
            row.set_title('{}'.format(lights[index]['name']))
            row.add(status_row)
            row.add(brightness_row)
            row.show()
            self.lights_preference_group.add(row)

    def update_bridge_stack_view(self, config):
        name_label = Gtk.Label()
        name_label.set_label(config['name'])
        name_label.show()
        name_row = Handy.ActionRow()
        name_row.set_title('Name')
        name_row.add(name_label)
        name_row.show()
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
        self.bridge_info_preference_group.add(name_row)
        self.bridge_info_preference_group.add(ipaddress_row)
        self.bridge_info_preference_group.add(mac_row)
        self.bridge_info_preference_group.add(bridgeid_row)
        self.bridge_info_preference_group.add(timezone_row)

    def update_groups_stack_view(self, groups, bridge, device_id):
        for index in groups:
            switch = Gtk.Switch()
            switch.set_active(groups[index]['action']['on'])
            switch.connect("notify::active", self.on_groups_switch_activated, bridge, device_id, index)
            switch.set_valign(Gtk.Align.CENTER)
            switch.show()
            status_row = Handy.ActionRow()
            status_row.set_title('Accendi Gruppo')
            status_row.add(switch)
            status_row.show()
            preference_group = Handy.PreferencesGroup()
            preference_group.set_title(groups[index]['name'])
            preference_group.add(status_row)
            preference_group.show()
            self.groups_preferences_page.add(preference_group)

