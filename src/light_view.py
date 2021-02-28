import gi

gi.require_version('Handy', '1')

from .rest_utilities import RESTUtilities
from gi.repository import Gtk, Handy

@Gtk.Template(resource_path='/org/scroker/LightController/light_view.ui')
class LightExpanderRow(Handy.ExpanderRow):
    __gtype_name__ = 'LightExpanderRow'

    light_brightness_ad = Gtk.Template.Child()
    light_brightness_scale = Gtk.Template.Child()

    def __init__(self, bridge, auth_handler, light, index):
        super().__init__()
        self.set_title(light['name'])
        self.set_enable_expansion(light['state']['on'])
        self.connect("notify::enable-expansion", self.on_light_expander_switch_activated, bridge, auth_handler, index)
        self.light_brightness_ad.set_value(light['state']['bri'])
        self.light_brightness_scale.connect("value-changed", self.on_light_scale_moved, bridge, auth_handler, index)

    # Light GtkScale on scale signal functions
    def on_light_scale_moved(self, widget, bridge, auth_handler, index):
        RESTUtilities.put_light_status(bridge, auth_handler, index, brightness=int(widget.get_value()))

    def on_light_expander_switch_activated(self, widget, event, bridge, auth_handler, index):
        if widget.get_enable_expansion():
            RESTUtilities.put_light_status(bridge, auth_handler, index, active=True)
        else :
            RESTUtilities.put_light_status(bridge, auth_handler, index, active=False)

