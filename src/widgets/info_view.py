import gi

gi.require_version('Handy', '1')

from gi.repository import Gtk, Handy

@Gtk.Template(resource_path='/org/scroker/LightController/widgets/info_view.ui')
class LightControllerAboutDialog(Gtk.AboutDialog):
    __gtype_name__ = 'LightControllerAboutDialog'

    def __init__(self):
        super().__init__()
