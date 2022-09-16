import gi

from gi.repository import Gtk

@Gtk.Template(resource_path='/org/gnome/House/widgets/info_view.ui')
class LightControllerAboutDialog(Gtk.AboutDialog):
    __gtype_name__ = 'LightControllerAboutDialog'

    def __init__(self):
        super().__init__()
