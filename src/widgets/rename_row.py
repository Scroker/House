import gi

gi.require_version('Adw', '1')

from .utilities import RESTUtilities
from gi.repository import Gtk, Adw

@Gtk.Template(resource_path='/org/gnome/House/widgets/rename_row.ui')
class RenameRowWidget(Adw.PreferencesRow):
    __gtype_name__ = 'RenameRowWidget'

    light_rename_entry = Gtk.Template.Child()
    light_modify_action_row = Gtk.Template.Child()
    light_rename_action_row = Gtk.Template.Child()

    def __init__(self, bridge, auth_handler, light, index, control_row):
        super().__init__()
        self.light_modify_action_row.set_title(light['name'])
        self.control_row = control_row
        self.index = index
        self.bridge = bridge
        self.auth_handler = auth_handler
        self.light = light

    @Gtk.Template.Callback()
    def on_light_rename_button(self, widget):
        self.light_modify_action_row.set_visible(False)
        self.light_rename_action_row.set_visible(True)

    @Gtk.Template.Callback()
    def on_light_delete_button(self, widget):
        self.control_row.destroy()
        self.destroy()

    @Gtk.Template.Callback()
    def on_cancel_rename_button(self, widget):
        self.light_modify_action_row.set_visible(True)
        self.light_rename_entry.set_text('')
        self.light_rename_action_row.set_visible(False)

    @Gtk.Template.Callback()
    def on_apply_rename_button(self, widget):
        if len(self.light_rename_entry.get_text()) > 4:
            self.light_modify_action_row.set_visible(True)
            self.light_modify_action_row.set_title(self.light_rename_entry.get_text())
            self.control_row.set_title(self.light_rename_entry.get_text())
            try:
                RESTUtilities.put_light_name(self.bridge, self.auth_handler, self.index, self.light_rename_entry.get_text())
            except Exception:
                print('Hello world')
            self.light_rename_entry.set_text('')
            self.light_rename_action_row.set_visible(False)




