from gi.repository import GObject
from zeroconf import ServiceListener, ServiceBrowser, Zeroconf

class AuthenticationHandler(GObject.Object):

    def __init__(self, user_name):
        GObject.GObject.__init__(self)
        self.user_name = user_name

class Bridge(GObject.Object):

    def __init__(self, bridge_id, internal_ip_address):
        GObject.GObject.__init__(self)
        self.bridge_id = bridge_id
        self.internal_ip_address = internal_ip_address

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

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        self.name = name
        self.info = zc.get_service_info(type_, name)
        print(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        self.name = name
        self.info = zc.get_service_info(type_, name)
        print(f"Service {name} added")
