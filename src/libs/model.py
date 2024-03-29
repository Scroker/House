from gi.repository import GObject
from zeroconf import ServiceListener, ServiceBrowser, Zeroconf
from .hueutilities import HueServicesREST

class AuthenticationHandler(GObject.Object):
    __gtype_name__ = 'AuthenticationHandler'

    def __init__(self, user_name):
        GObject.GObject.__init__(self)
        self.user_name = user_name

class Bridge(GObject.Object):
    __gtype_name__ = 'Bridge'

    def __init__(self, name, ip_address):
        GObject.GObject.__init__(self)
        self.name = name
        self.ip_address = ip_address
        self.macaddress = None
        self.swversion = None
        self.bridgeid = None
        self.macaddress = None
        self.dhcp = None
        self.proxyaddress = None
        self.proxyport = None
        self.modelid = None
        self.UTC = None
        self.timezone = None
        self.modelid = None
        self.datastoreversion = None
        self.swversion = None
        self.linkbutton = None
        self.portalservices = None
        self.portalconnection = None
        self.starterkitid = None


    def get_config(self, authentication_handler:AuthenticationHandler):
        json = HueServicesREST.get_config(self.ip_address, authentication_handler.user_name)
        self.macaddress = json['mac']
        self.swversion = json['zigbeechannel']
        self.bridgeid = json['bridgeid']
        self.macaddress = json['mac']
        self.dhcp = json['dhcp']
        self.proxyaddress = json['proxyaddress']
        self.proxyport = json['proxyport']
        self.modelid = json['UTC']
        self.UTC = json['localtime']
        self.timezone = json['timezone']
        self.modelid = json['modelid']
        self.datastoreversion = json['datastoreversion']
        self.swversion = json['swversion']
        self.linkbutton = json['linkbutton']
        self.portalservices = json['portalservices']
        self.portalconnection = json['portalconnection']
        self.starterkitid = json['starterkitid']

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

class MyClass(GObject.Object):
    __gtype_name__ = 'MyClass'

    def __init__(self):
        GObject.GObject.__init__(self)

    @GObject.Signal(flags=GObject.SignalFlags.RUN_LAST, return_type=bool,
                    arg_types=(object,),
                    accumulator=GObject.signal_accumulator_true_handled)

    def light_selected_signal(self, *args):
        print("Selected light: " + args[0].name)

class Constants(GObject.Object):
    __gtype_name__ = 'Constants'

    APPLICATION_STYLE = '/org/gnome/House/style.css'

    def __init__(self, user_name):
        GObject.GObject.__init__(self)


