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
from .utilities import RESTUtilities
from .model import Bridge
from .model import AuthenticationHandler
from .add_view import AddPreferenceGroup
from .group_view import GroupViewPreferenceGroup
from .info_view import LightControllerAboutDialog
from .light_view import LightPreferencesRow
from .bridge_view import BridgePreferenceGroup
from .rename_row import RenameRowWidget

@Gtk.Template(resource_path='/org/gnome/House/window.ui')
class House(Adw.ApplicationWindow):
    __gtype_name__ = 'House'

    rename_rows = []
    control_rows = []
    groups_preferences = []
    main_stack = Gtk.Template.Child()
    connect_button = Gtk.Template.Child()
    press_button_label = Gtk.Template.Child()
    headerbar_switcher = Gtk.Template.Child()
    headerbar_add_button = Gtk.Template.Child()
    lights_preference_page = Gtk.Template.Child()
    bridge_preference_page = Gtk.Template.Child()
    #headerbar_info_button = Gtk.Template.Child()
    groups_preferences_page = Gtk.Template.Child()
    headerbar_enable_modification_button = Gtk.Template.Child()
    settings = Gio.Settings.new('org.gnome.House')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bridge = Bridge(self.settings.get_string('hue-hub-id'), self.settings.get_string('hue-hub-ip-address'))
        self.auth_handler = AuthenticationHandler(self.settings.get_string('hue-hub-user-name'))
        self.add_group_preference_group = AddPreferenceGroup(self.bridge, self.auth_handler)
        self.groups_preferences_page.add(self.add_group_preference_group)
        try:
            self.update_stack_view()
        except Exception as error:
            self.connect_button.set_sensitive(True)

    # GtkStackView update functions
    def update_stack_view(self):
        config = RESTUtilities.get_config(self.bridge, self.auth_handler)
        self.update_bridge_stack_view(config)
        lights = RESTUtilities.get_lights(self.bridge, self.auth_handler)
        self.update_light_stack_view(lights, self.bridge, self.auth_handler)
        groups = RESTUtilities.get_groups(self.bridge, self.auth_handler)
        self.update_groups_stack_view(groups, self.bridge, self.auth_handler)

    def update_light_stack_view(self, lights, bridge, auth_handler):
        preference_group = Handy.PreferencesGroup()
        preference_group.set_title('Luci')
        for light_id in lights :
            control_row = LightPreferencesRow(bridge, auth_handler, lights[light_id], light_id)
            rename_row = RenameRowWidget(bridge, auth_handler, lights[light_id], light_id, control_row)
            self.control_rows.append(control_row)
            self.rename_rows.append(rename_row)
            preference_group.add(control_row)
            preference_group.add(rename_row)
        preference_group.show()
        self.lights_preference_page.add(preference_group)

    def update_groups_stack_view(self, groups, bridge, auth_handler):
        for index in groups:
            preference_group = GroupViewPreferenceGroup(bridge, auth_handler, groups[index], index)
            self.groups_preferences.append(preference_group)
            self.groups_preferences_page.add(preference_group)

    def update_bridge_stack_view(self, config):
        preference_group = BridgePreferenceGroup(config)
        self.bridge_preference_page.add(preference_group)

    #@Gtk.Template.Callback()
    #def on_info_button(self, widget):
    #    about_dialog = LightControllerAboutDialog()
    #    about_dialog.show()

    @Gtk.Template.Callback()
    def on_stack_change(self, widget, arg):
        if widget.get_visible_child_name() == 'lights' or widget.get_visible_child_name() == 'bridge':
            self.headerbar_add_button.set_visible(False)
        else :
            self.headerbar_add_button.set_visible(True)

    @Gtk.Template.Callback()
    def on_add_modifications(self, widget):
        if not widget.get_active() :
            self.add_group_preference_group.set_visible(False)
        else :
            self.add_group_preference_group.set_visible(True)

    @Gtk.Template.Callback()
    def on_enable_modifications(self, widget):
        for index in range(len(self.rename_rows)) :
            if not widget.get_active() :
                self.rename_rows[index].set_visible(False)
                self.control_rows[index].set_visible(True)
            else :
                self.rename_rows[index].set_visible(True)
                self.control_rows[index].set_visible(False)
        for index in range(len(self.groups_preferences)):
            if not widget.get_active() :
                self.groups_preferences[index].group_modify_action_row.set_visible(False)
                self.groups_preferences[index].group_rename_action_row.set_visible(False)
                self.groups_preferences[index].group_expander_row.set_visible(True)
                self.groups_preferences[index].groups_lights_expander_row.set_visible(True)
            else :
                self.groups_preferences[index].group_modify_action_row.set_visible(True)
                self.groups_preferences[index].group_rename_action_row.set_visible(False)
                self.groups_preferences[index].group_expander_row.set_visible(False)
                self.groups_preferences[index].groups_lights_expander_row.set_visible(False)

    @Gtk.Template.Callback()
    def on_connect_button(self, widget):
        for bridge in RESTUtilities.discover_bridges():
            try:
                device_name = socket.gethostname() + "#" + platform.system()
                print(device_name)
                auth_handler = RESTUtilities.pair_with_the_bridge(bridge, device_name)
                print(auth_handler.user_name)
                #self.update_stack_view(bridge, auth_handler)
                self.settings.set_string('hue-hub-id', bridge.bridge_id)
                self.settings.set_string('hue-hub-ip-address', bridge.internal_ip_address)
                self.settings.set_string('hue-hub-user-name', auth_handler.user_name)
                self.connect_button.set_sensitive(False)
                self.press_button_label.set_visible(False)
                print("Label Hidden")
                break
            except Exception as error:
                if '\'type\': 101' in str(error) :
                    self.press_button_label.set_visible(True)


