from gi.repository import GObject
from zeroconf import ServiceListener, ServiceBrowser, Zeroconf

class AuthenticationHandler(GObject.Object):

    def __init__(self, user_name):
        GObject.GObject.__init__(self)
        self.user_name = user_name

class Bridge(GObject.Object):

    def __init__(self, bridge_id, internal_ip_address):
        GObject.GObject.__init__(self)
        self.name = bridge_id
        self.internal_ip_address = internal_ip_address

class Group(GObject.Object):

    def __init__(self, light_id, name, light_type, model, manufacter, unique_id, sw_version):
        GObject.GObject.__init__(self)
        self.id = light_id
        self.name = name
        self.type = light_type
        self.model = model
        self.manufacter = manufacter
        self.unique_id = unique_id
        self.sw_version = sw_version


class Light(GObject.Object):

    def __init__(self, light_id, name, model, manufacter, unique_id, sw_version):
        GObject.GObject.__init__(self)
        self.id = light_id
        self.name = name
        self.model = model
        self.manufacter = manufacter
        self.unique_id = unique_id
        self.sw_version = sw_version

class PhilipsHueListener(ServiceListener):

    def __init__(self):
        self.info = None
        self.name = None
        zeroconf = Zeroconf()
        browser = ServiceBrowser(zeroconf, "_hue._tcp.local.", self)
        while True:
            if self.info != None: break
        zeroconf.close()

    def get_ip_addresses(self):
        if self.info != None:
            return self.info.parsed_addresses()

    def get_bridge(self) -> Bridge:
        bridge = Bridge(self.name, self.info.parsed_addresses()[0])
        return bridge

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        self.name = name
        self.info = zc.get_service_info(type_, name)
        print(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        self.name = name.removesuffix('._hue._tcp.local.')
        self.info = zc.get_service_info(type_, name)
        print(f"Service {name} added")

class Constants(GObject.Object):

    APPLICATION_STYLE = '/org/gnome/House/style.css'

    def __init__(self, user_name):
        GObject.GObject.__init__(self)
