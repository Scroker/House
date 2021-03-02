import gi

gi.require_version('Handy', '1')

from .utilities import RESTUtilities
from gi.repository import Gtk, Handy

@Gtk.Template(resource_path='/org/scroker/LightController/widgets/add_view.ui')
class AddPreferenceGroup(Handy.PreferencesGroup):
    __gtype_name__ = 'AddPreferenceGroup'

    new_group_name_entry = Gtk.Template.Child()

    def __init__(self, bridge, auth_handler):
        super().__init__()
        self.bridge = bridge
        self.auth_handler = auth_handler

    @Gtk.Template.Callback()
    def on_new_group_name__button(self, widget):
        group_name = self.new_group_name_entry.get_text()
        index = RESTUtilities.post_new_group(self.bridge, self.auth_handler, group_name)
        group = RESTUtilities.get_group(self.bridge, self.auth_handler, index)
        self.new_group_name_entry.set_text('')

