import gi

gi.require_version('Handy', '1')

from gi.repository import Gtk, Handy
from .utilities import RESTUtilities

@Gtk.Template(resource_path='/org/scroker/LightController/widgets/group_view.ui')
class GroupViewPreferenceGroup(Handy.PreferencesGroup):
    __gtype_name__ = 'GroupViewPreferenceGroup'

    groups_lights_expander_row = Gtk.Template.Child()
    group_expander_row = Gtk.Template.Child()
    group_light_scale = Gtk.Template.Child()
    group_light_adjustment = Gtk.Template.Child()
    group_rename_entry = Gtk.Template.Child()
    group_modify_action_row = Gtk.Template.Child()
    group_rename_action_row = Gtk.Template.Child()
    group_rename_button = Gtk.Template.Child()
    group_rename_entry = Gtk.Template.Child()
    apply_group_rename_button = Gtk.Template.Child()
    cancel_group_rename_button = Gtk.Template.Child()
    group_delete_button = Gtk.Template.Child()

    def __init__(self, bridge, auth_handler, group, index):
        super().__init__()
        self.set_title(group['name'])
        self.apply_group_rename_button.connect('clicked', self.on_apply_rename_button, bridge, auth_handler, index)
        self.cancel_group_rename_button.connect('clicked', self.on_cancel_rename_button)
        self.group_delete_button.connect('clicked', self.on_delete_group_button, bridge, auth_handler, index)
        self.group_rename_button.connect('clicked', self.on_group_rename_button)
        self.group_light_scale.connect("value-changed", self.on_groups_light_scale_moved, bridge, auth_handler, index)
        if 'bri' in group['action']:
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

    def on_delete_group_button(self, widget, bridge, authentication_handler, index):
        RESTUtilities.delete_group(bridge, authentication_handler, index)
        self.destroy()

    def on_cancel_rename_button(self, widget):
        self.group_modify_action_row.set_visible(True)
        self.group_rename_entry.set_text('')
        self.group_rename_action_row.set_visible(False)

    def on_apply_rename_button(self, widget, bridge, auth_handler, index):
        if len(self.group_rename_entry.get_text()) > 4:
            self.group_modify_action_row.set_visible(True)
            self.set_title(self.group_rename_entry.get_text())
            RESTUtilities.put_group_name(bridge, auth_handler, index, self.group_rename_entry.get_text())
            self.group_rename_entry.set_text('')
            self.group_rename_action_row.set_visible(False)

    def on_group_rename_button(self, widget):
        self.group_modify_action_row.set_visible(False)
        self.group_rename_action_row.set_visible(True)


    def on_groups_light_scale_moved(self, widget, bridge, auth_handler, index):
        RESTUtilities.put_group_action(bridge, auth_handler, index, brightness=int(widget.get_value()))

    def on_groups_expander_switch_activated(self, widget, event, bridge, auth_handler, index):
        if widget.get_enable_expansion():
            RESTUtilities.put_group_action(bridge, auth_handler, index, active=True)
        else :
            RESTUtilities.put_group_action(bridge, auth_handler, index, active=False)

    def on_light_switch_activated(self, widget, event, bridge, auth_handler, index):
        if widget.get_active():
            RESTUtilities.put_light_status(bridge, auth_handler, index, active=True)
        else :
            RESTUtilities.put_light_status(bridge, auth_handler, index, active=False)


  
