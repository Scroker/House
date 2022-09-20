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

    connected_button = Gtk.Template.Child()
    disconnected_button = Gtk.Template.Child()
    toast_overlay = None

    def __init__(self, toast_overlay, listener):
        super().__init__()
        self.toast_overlay = toast_overlay
        self.set_title(listener.name.removesuffix('._hue._tcp.local.'))
        print(listener.info.parsed_addresses()[0])
        self.set_subtitle(listener.info.parsed_addresses()[0])
        self.connected_button.set_visible(False)

    @Gtk.Template.Callback()
    def on_bridge_connect(self, widget):
        toast = Adw.Toast()
        toast.set_title('Hold the button on the bridge')
        self.toast_overlay.add_toast(toast)

@Gtk.Template(resource_path='/org/gnome/House/widgets/light_page.ui')
class LightPage(Gtk.Box):
    __gtype_name__ = 'LightPage'

    def __init__(self):
        super().__init__()

    @Gtk.Template.Callback()
    def on_modify_name_click(self, widget):
        print("Name modified")
