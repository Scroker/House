import gi

from gi.repository import Gtk, Gio, Adw
from .model import Light, Group, Bridge, AuthenticationHandler
from .invenctory import AuthenticationProvider, LightsInvenctory

@Gtk.Template(resource_path='/org/gnome/House/widgets/light_action_row.ui')
class LightActionRow(Adw.ActionRow):
    __gtype_name__ = 'LightActionRow'

    def __init__(self, light:Light):
        super().__init__()
        self.set_title(light.name)
        self.set_subtitle(light.type)

    @Gtk.Template.Callback()
    def on_activate(self, widget):
        print(self.get_title())

@Gtk.Template(resource_path='/org/gnome/House/widgets/group_action_row.ui')
class GroupActionRow(Adw.ActionRow):
    __gtype_name__ = 'GroupActionRow'

    def __init__(self, group:Group):
        super().__init__()
        self.set_title(group.name)
        self.set_subtitle(group.type)

    @Gtk.Template.Callback()
    def on_activate(self, widget):
        print(self.get_title())

@Gtk.Template(resource_path='/org/gnome/House/widgets/bridge_action_row.ui')
class BridgeActionRow(Adw.ActionRow):
    __gtype_name__ = 'BridgeActionRow'

    connected_button = Gtk.Template.Child()
    disconnected_button = Gtk.Template.Child()

    def __init__(self, settings:Gio.Settings, toast_overlay:Adw.ToastOverlay, bridge:Bridge):
        super().__init__()
        self.toast_overlay = toast_overlay
        self.bridge = bridge
        self.settings = settings
        self.set_title(bridge.name)
        self.set_subtitle(bridge.internal_ip_address)
        if self.settings.get_string('hue-hub-id') == bridge.name and self.settings.get_string('hue-hub-ip-address') == bridge.internal_ip_address:
            self.disconnected_button.set_visible(False)
        else:
            self.connected_button.set_visible(False)

    @Gtk.Template.Callback()
    def on_activate(self, widget):
        print(self.bridge.name)

    @Gtk.Template.Callback()
    def on_bridge_connect(self, widget):
        try:
            auth_handler = AuthenticationProvider.autenticate(self.bridge)
            self.settings.set_string('hue-hub-id', self.bridge.name)
            self.settings.set_string('hue-hub-ip-address', self.bridge.internal_ip_address)
            self.settings.set_string('hue-hub-user-name', auth_handler.user_name)
            self.connected_button.set_visible(True)
            self.disconnected_button.set_visible(False)
            toast = Adw.Toast()
            toast.set_title('Connected with ' + self.bridge.name)
            self.toast_overlay.add_toast(toast)
        except Exception as err:
            toast = Adw.Toast()
            toast.set_title('Error: ' + err.args[0])
            self.toast_overlay.add_toast(toast)

    @Gtk.Template.Callback()
    def on_bridge_disconnect(self, widget):
        self.settings.set_string('hue-hub-id', '')
        self.settings.set_string('hue-hub-ip-address', '')
        self.settings.set_string('hue-hub-user-name', '')
        self.connected_button.set_visible(False)
        self.disconnected_button.set_visible(True)
        toast = Adw.Toast()
        toast.set_title('Disonnected from ' + self.bridge.name)
        self.toast_overlay.add_toast(toast)

@Gtk.Template(resource_path='/org/gnome/House/widgets/light_page.ui')
class LightPage(Adw.PreferencesPage):
    __gtype_name__ = 'LightPage'
    light_name = Gtk.Template.Child()
    light_model = Gtk.Template.Child()
    light_type = Gtk.Template.Child()
    manufacturer_name = Gtk.Template.Child()
    unique_id = Gtk.Template.Child()
    sw_version = Gtk.Template.Child()

    def __init__(self, light:Light):
        super().__init__()
        self.light_name.set_label(light.name)
        self.light_model.set_label(light.model)
        self.light_type.set_label(light.type)
        self.manufacturer_name.set_label(light.manufacturer_name)
        self.unique_id.set_label(light.unique_id)
        self.sw_version.set_label(light.sw_version)


