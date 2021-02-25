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

@Gtk.Template(resource_path='/org/scroker/LightController/press-connect-button.ui')
class BridgeConnectionProblemDialog(Gtk.Dialog):
    __gtype_name__ = 'BridgeConnectionProblemDialog'

    try_count = 0
    device_id = None
    utility = BrigdeUtilities()
    cancel_button = Gtk.Template.Child()
    retry_button = Gtk.Template.Child()
    warning_message = Gtk.Template.Child()

    def __init__(self, parent, bridge):
        super().__init__(self, title="My Dialog", transient_for=parent, flags=0)
        self.connect('delete_event', self.on_destroy)
        self.cancel_button.connect('clicked', self.on_destroy)
        self.cancel_button.get_style_context().add_class(Gtk.STYLE_CLASS_DESTRUCTIVE_ACTION)
        self.retry_button.connect('clicked', self.retry_connect_button, bridge)
        self.retry_button.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        self.set_default_size(150, 100)
        self.show_all()

    def retry_connect_button(self, button, bridge):
        self.try_count += 1
        try:
            self.device_id = self.utility.pair_with_the_bridge(bridge)
            self.destroy()
        except Exception as error:
            self.warning_message.set_label(str(error) + " " + str(self.try_count))

    def on_destroy(self, widget, event=None):
        self.destroy()

@Gtk.Template(resource_path='/org/scroker/LightController/window.ui')
class LightcontrollerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'LightcontrollerWindow'

    Handy.init()
    squeezer = Gtk.Template.Child()
    headerbar_switcher = Gtk.Template.Child()
    bottom_switcher = Gtk.Template.Child()
    bridge_mac_label = Gtk.Template.Child()
    bridge_id_label = Gtk.Template.Child()
    bridge_api_key_label = Gtk.Template.Child()
    bridge_ip_address_label = Gtk.Template.Child()
    lights_preference_group = Gtk.Template.Child()
    bridge_name_label = Gtk.Template.Child()
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
                self.bridge_api_key_label.set_label("{}".format(device_id))
                self.update_bridge_stack_view(config)
                lights = self.utility.get_lights(bridge, device_id)
                self.update_light_stack_view(lights, bridge, device_id)
            except Exception as error:
                self.connect_button.set_sensitive(True)
                self.connect_button.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

    def on_headerbar_squeezer_notify(self, squeezer, event):
	    child = squeezer.get_visible_child()
	    self.bottom_switcher.set_reveal(child != self.headerbar_switcher)

    def update_light_stack_view(self, lights, bridge, device_id):
        for index in lights :
            brightness_ad = Gtk.Adjustment(lights[index]['state']['bri'], 0, 254, 5, 10, 0)
            brightness_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=brightness_ad)
            brightness_scale.connect("value-changed", self.scale_moved, bridge, device_id, index)
            brightness_scale.set_valign(Gtk.Align.START)
            brightness_scale.set_digits(False)
            brightness_scale.set_hexpand(True)
            brightness_scale.set_sensitive(lights[index]['state']['on'])
            brightness_scale.show()
            switch = Gtk.Switch()
            switch.set_active(lights[index]['state']['on'])
            switch.connect("notify::active", self.on_switch_activated, bridge, device_id, index, brightness_scale)
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

    def scale_moved(self, widget, bridge, device_id, index):
        self.utility.set_light_brightness(bridge, device_id, index, int(widget.get_value()))

    def on_switch_activated(self, widget, event, bridge, device_id, index, brightness_scale):
        if widget.get_active():
            self.utility.set_light_status(bridge, device_id, index, True)
            brightness_scale.set_sensitive(True)
        else :
            self.utility.set_light_status(bridge, device_id, index, False)
            brightness_scale.set_sensitive(False)

    def update_bridge_stack_view(self, config):
        self.bridge_ip_address_label.set_label('{}'.format(config['ipaddress']))
        self.bridge_name_label.set_label('{}'.format(config['name']))
        self.bridge_mac_label.set_label('{}'.format(config['mac']))
        self.bridge_id_label.set_label('{}'.format(config['bridgeid']))

    def on_connect_button(self, button, bridge):
            try:
                device_id = self.utility.pair_with_the_bridge(bridge)
                self.settings.set_string('device-id', device_id)
                config = self.utility.get_config(bridge, device_id)
                self.bridge_api_key_label.set_label('{}'.format(device_id))
                self.update_bridge_stack_view(config)
                lights = self.utility.get_lights(bridge, device_id)
                self.update_light_stack_view(lights, bridge, device_id)
                self.connect_button.set_sensitive(False)
            except Exception as error:
                dialog = BridgeConnectionProblemDialog(self, bridge)
                dialog.warning_message.set_label(str(error))
                dialog.run()
                if dialog.device_id != None :
                    self.settings.set_string('device-id', dialog.device_id)
                    self.bridge_api_key_label.set_label('{}'.format(dialog.device_id))
                    config = self.utility.get_config(bridge, dialog.device_id)
                    self.update_bridge_stack_view(config)
                    lights = self.utility.get_lights(bridge, dialog.device_id)
                    self.update_light_stack_view(lights, bridge, dialog.device_id)
                    self.connect_button.set_sensitive(False)




