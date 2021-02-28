import gi

gi.require_version('Handy', '1')

from .rest_utilities import RESTUtilities
from gi.repository import Gtk, Handy

@Gtk.Template(resource_path='/org/scroker/LightController/group_view.ui')
class GroupViewPreferenceGroup(Handy.PreferencesGroup):
    __gtype_name__ = 'GroupViewPreferenceGroup'

    groups_lights_expander_row = Gtk.Template.Child()
    add_light_action_row = Gtk.Template.Child()
    group_expander_row = Gtk.Template.Child()
    group_light_scale = Gtk.Template.Child()
    group_light_adjustment = Gtk.Template.Child()
    rest_utility = RESTUtilities()

    def __init__(self, bridge, auth_handler, group, index):
        super().__init__()
        self.set_title(group['name'])
        self.group_light_scale.connect("value-changed", self.on_groups_light_scale_moved, bridge, auth_handler, index)
        self.group_light_scale.set_value(group['action']['bri'])
        self.group_expander_row.connect("notify::enable-expansion", self.on_groups_expander_switch_activated, bridge, auth_handler, index)
        self.group_expander_row.set_enable_expansion(group['action']['on'])
        lights = group['lights']
        for light_id in lights:
            switch = Gtk.Switch()
            switch.connect("notify::active", self.on_light_switch_activated, bridge, auth_handler, light_id)
            switch.set_active(lights[light_id]['state']['on'])
            switch.set_valign(Gtk.Align.CENTER)
            switch.show()
            row = Handy.ActionRow()
            row.set_title(lights[light_id]['name'])
            row.add(switch)
            row.show()
            self.groups_lights_expander_row.add(row)

    def on_groups_light_scale_moved(self, widget, bridge, auth_handler, index):
        self.rest_utility.put_group_action(bridge, auth_handler, index, brightness=int(widget.get_value()))

    def on_groups_expander_switch_activated(self, widget, event, bridge, auth_handler, index):
        if widget.get_enable_expansion():
            self.rest_utility.put_group_action(bridge, auth_handler, index, active=True)
        else :
            self.rest_utility.put_group_action(bridge, auth_handler, index, active=False)

    def on_light_switch_activated(self, widget, event, bridge, auth_handler, index):
        if widget.get_active():
            self.rest_utility.put_light_status(bridge, auth_handler, index, active=True)
        else :
            self.rest_utility.put_light_status(bridge, auth_handler, index, active=False)


  
