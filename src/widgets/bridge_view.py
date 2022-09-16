import gi

gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw

@Gtk.Template(resource_path='/org/gnome/House/widgets/bridge_view.ui')
class BridgePreferenceGroup(Adw.PreferencesGroup):
    __gtype_name__ = 'BridgePreferenceGroup'

    bridge_ip_address = Gtk.Template.Child()
    bridge_mac_address = Gtk.Template.Child()
    bridge_id = Gtk.Template.Child()
    bridge_time_zone = Gtk.Template.Child()
    groups_lights_expander_row = Gtk.Template.Child()

    def __init__(self, config):
        super().__init__()
        self.set_title(config['name'])
        self.bridge_id.set_label(config['bridgeid'])
        self.bridge_ip_address.set_label(config['ipaddress'])
        self.bridge_mac_address.set_label(config['mac'])
        self.bridge_time_zone.set_label(config['timezone'])
        for api_key in config['whitelist']:
            label = Gtk.Label()
            label.set_label(config['whitelist'][api_key]['last use date'])
            label.show()
            row = Adw.ActionRow()
            row.set_title(config['whitelist'][api_key]['name'])
            row.add(label)
            row.show()
            self.groups_lights_expander_row.add(row)

