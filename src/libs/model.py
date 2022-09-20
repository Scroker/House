from gi.repository import GObject
from zeroconf import ServiceListener, ServiceBrowser, Zeroconf

class AuthenticationHandler(GObject.Object):
    __gtype_name__ = 'AuthenticationHandler'

    def __init__(self, user_name):
        GObject.GObject.__init__(self)
        self.user_name = user_name

class Bridge(GObject.Object):
    __gtype_name__ = 'Bridge'

    def __init__(self, bridge_id, internal_ip_address):
        GObject.GObject.__init__(self)
        self.name = bridge_id
        self.internal_ip_address = internal_ip_address

class Group(GObject.Object):
    __gtype_name__ = 'Group'

    def __init__(self, group_id, name, group_type):
        GObject.GObject.__init__(self)
        self.id = group_id
        self.name = name
        self.type = group_type

class Light(GObject.Object):
    __gtype_name__ = 'Light'

    def __init__(self, light_id, name, light_type, model, manufacturer_name, unique_id, sw_version):
        GObject.GObject.__init__(self)
        self.id = light_id
        self.name = name
        self.type = light_type
        self.model = model
        self.manufacturer_name = manufacturer_name
        self.unique_id = unique_id
        self.sw_version = sw_version

class Constants(GObject.Object):
    __gtype_name__ = 'Constants'

    APPLICATION_STYLE = '/org/gnome/House/style.css'

    def __init__(self, user_name):
        GObject.GObject.__init__(self)
