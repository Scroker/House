import gi

gi.require_version('Handy', '1')

from .utilities import RESTUtilities
from gi.repository import Gtk, Handy

@Gtk.Template(resource_path='/org/scroker/LightController/light_view.ui')
class LightExpanderRow(Handy.ExpanderRow):
    __gtype_name__ = 'LightExpanderRow'

    light_rename_entry = Gtk.Template.Child()
    light_brightness_ad = Gtk.Template.Child()
    light_rename_button = Gtk.Template.Child()
    light_brightness_scale = Gtk.Template.Child()
    light_modify_action_row = Gtk.Template.Child()
    light_rename_action_row = Gtk.Template.Child()
    apply_light_rename_button = Gtk.Template.Child()
    cancel_light_rename_button = Gtk.Template.Child()
    delete_light_button = Gtk.Template.Child()

    def __init__(self, bridge, auth_handler, light, index):
        super().__init__()
        self.set_title(light['name'])
        self.set_enable_expansion(light['state']['on'])
        self.connect("notify::enable-expansion", self.on_light_expander_switch_activated, bridge, auth_handler, index)
        self.light_brightness_ad.set_value(light['state']['bri'])
        self.light_brightness_scale.connect("value-changed", self.on_light_scale_moved, bridge, auth_handler, index)
        self.apply_light_rename_button.connect('clicked', self.on_apply_rename_button, bridge, auth_handler, index)
        self.cancel_light_rename_button.connect('clicked', self.on_cancel_rename_button)
        self.delete_light_button.connect('clicked', self.on_delete_light_button)
        self.light_rename_button.connect('clicked', self.on_light_rename_button)

    def on_delete_light_button(self, widget):
        self.destroy()

    def on_cancel_rename_button(self, widget):
        self.light_modify_action_row.set_visible(True)
        self.light_rename_entry.set_text('')
        self.light_rename_action_row.set_visible(False)

    def on_apply_rename_button(self, widget, bridge, auth_handler, index):
        if len(self.light_rename_entry.get_text()) > 4:
            self.light_modify_action_row.set_visible(True)
            self.set_title(self.light_rename_entry.get_text())
            RESTUtilities.put_light_name(bridge, auth_handler, index, self.light_rename_entry.get_text())
            self.light_rename_entry.set_text('')
            self.light_rename_action_row.set_visible(False)

    def on_light_rename_button(self, widget):
        self.light_modify_action_row.set_visible(False)
        self.light_rename_action_row.set_visible(True)

    # Light GtkScale on scale signal functions
    def on_light_scale_moved(self, widget, bridge, auth_handler, index):
        RESTUtilities.put_light_status(bridge, auth_handler, index, brightness=int(widget.get_value()))

    def on_light_expander_switch_activated(self, widget, event, bridge, auth_handler, index):
        if widget.get_enable_expansion():
            RESTUtilities.put_light_status(bridge, auth_handler, index, active=True)
        else :
            RESTUtilities.put_light_status(bridge, auth_handler, index, active=False)

