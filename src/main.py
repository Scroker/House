# main.py
#
# Copyright 2021 Giorgio Dramis
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, Gio

from .window import LightcontrollerWindow


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='org.scroker.LightController',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        style_provider = Gtk.CssProvider()
        style_provider.load_from_resource('/org/scroker/LightController/widgets/style.css')
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        win = self.props.active_window
        if not win:
            win = LightcontrollerWindow(application=self)
        win.present()

def main(version):
    app = Application()
    return app.run(sys.argv)
