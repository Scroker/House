import gi

gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw

@Gtk.Template(resource_path='/org/gnome/House/widgets/light_action_row.ui')
class LightActionRow(Adw.ActionRow):
    __gtype_name__ = 'LightActionRow'

    def __init__(self):
        super().__init__()

@Gtk.Template(resource_path='/org/gnome/House/widgets/group_action_row.ui')
class GroupActionRow(Adw.ActionRow):
    __gtype_name__ = 'GroupActionRow'

    def __init__(self):
        super().__init__()

@Gtk.Template(resource_path='/org/gnome/House/widgets/bridge_action_row.ui')
class BridgeActionRow(Adw.ActionRow):
    __gtype_name__ = 'BridgeActionRow'

    def __init__(self):
        super().__init__()


@Gtk.Template(resource_path='/org/gnome/House/widgets/light_page.ui')
class LightPage(Gtk.Box):
    __gtype_name__ = 'LightPage'

    def __init__(self):
        super().__init__()

    @Gtk.Template.Callback()
    def on_modify_name_click(self, widget):
        print("Name modified")
