import gi

gi.require_version('Handy', '1')

from .utilities import RESTUtilities
from gi.repository import Gtk, Handy

@Gtk.Template(resource_path='/org/scroker/LightController/widgets/rename_row.ui')
class RenameRowWidget(Handy.PreferencesRow):
    __gtype_name__ = 'RenameRowWidget'

    light_modify_action_row = Gtk.Template.Child()
    light_rename_action_row = Gtk.Template.Child()
    apply_light_rename_button = Gtk.Template.Child()
    cancel_light_rename_button = Gtk.Template.Child()
    delete_light_button = Gtk.Template.Child()
    light_rename_entry = Gtk.Template.Child()
    light_rename_button = Gtk.Template.Child()

    def __init__(self, bridge, auth_handler, light, index, control_row):
        super().__init__()
        self.apply_light_rename_button.connect('clicked', self.on_apply_rename_button, bridge, auth_handler, index, control_row)
        self.cancel_light_rename_button.connect('clicked', self.on_cancel_rename_button)
        self.light_modify_action_row.set_title(light['name'])
        self.delete_light_button.connect('clicked', self.on_delete_light_button, control_row)
        self.light_rename_button.connect('clicked', self.on_light_rename_button)

    def on_delete_light_button(self, widget, control_row):
        control_row.destroy()
        self.destroy()

    def on_cancel_rename_button(self, widget):
        self.light_modify_action_row.set_visible(True)
        self.light_rename_entry.set_text('')
        self.light_rename_action_row.set_visible(False)

    def on_apply_rename_button(self, widget, bridge, auth_handler, index, control_row):
        if len(self.light_rename_entry.get_text()) > 4:
            self.light_modify_action_row.set_visible(True)
            self.light_modify_action_row.set_title(self.light_rename_entry.get_text())
            control_row.set_title(self.light_rename_entry.get_text())
            RESTUtilities.put_light_name(bridge, auth_handler, index, self.light_rename_entry.get_text())
            self.light_rename_entry.set_text('')
            self.light_rename_action_row.set_visible(False)

    def on_light_rename_button(self, widget):
        self.light_modify_action_row.set_visible(False)
        self.light_rename_action_row.set_visible(True)


