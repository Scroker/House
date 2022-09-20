import gi
import socket
import platform

gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw
from .model import Light, Bridge
from .utilities import RESTUtilities

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

    def __init__(self, app:Adw.ApplicationWindow, toast_overlay:Adw.ToastOverlay, bridge:Bridge):
        super().__init__()
        self.toast_overlay = toast_overlay
        self.bridge = bridge
        self.settings = app.settings
        self.set_title(bridge.name)
        self.set_subtitle(bridge.internal_ip_address)
        if self.settings.get_string('hue-hub-id') == bridge.name and self.settings.get_string('hue-hub-ip-address') == bridge.internal_ip_address:
            self.disconnected_button.set_visible(False)
        else:
            self.connected_button.set_visible(False)

    @Gtk.Template.Callback()
    def on_bridge_connect(self, widget):
        try:
            device_name = socket.gethostname() + "#" + platform.system()
            auth_handler = RESTUtilities.pair_with_the_bridge(self.bridge, device_name)
            self.settings.set_string('hue-hub-id', self.bridge.name)
            self.connected_button.set_visible(True)
            self.disconnected_button.set_visible(False)
            print(self.settings.get_string('hue-hub-id'))
            self.settings.set_string('hue-hub-ip-address', self.bridge.internal_ip_address)
            self.settings.set_string('hue-hub-user-name', auth_handler.user_name)
            print(self.settings.get_string('hue-hub-user-name'))
            self.connect_button.set_sensitive(False)
            self.press_button_label.set_visible(False)
            toast = Adw.Toast()
            toast.set_title('Connected!')
            self.toast_overlay.add_toast(toast)
        except Exception as err:
            toast = Adw.Toast()
            toast.set_title('Error: ' + err.args[0])
            self.toast_overlay.add_toast(toast)

@Gtk.Template(resource_path='/org/gnome/House/widgets/light_page.ui')
class LightPage(Adw.PreferencesPage):
    __gtype_name__ = 'LightPage'

    def __init__(self, light:Light):
        super().__init__()


