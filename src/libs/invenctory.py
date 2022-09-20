import socket
import platform

from gi.repository import GObject

from .model import Light, Group, Bridge, AuthenticationHandler
from .hueutilities import PhilipsHueListener, HueServicesREST

class AuthenticationProvider(GObject.Object):
    __gtype_name__ = 'AuthInvectory'

    def __init__(self):
        GObject.GObject.__init__(self)

    @staticmethod
    def autenticate(bridge:Bridge) -> AuthenticationHandler:
        device_name = socket.gethostname() + "#" + platform.system()
        auth_handler = HueServicesREST.pair_with_the_bridge(bridge, device_name)
        return auth_handler

class LightsInvenctory(GObject.Object):
    __gtype_name__ = 'LightsInvectory'

    def __init__(self):
        GObject.GObject.__init__(self)

    @staticmethod
    def get_lights(bridge:Bridge, authentication_handler:AuthenticationHandler):
        lights = []
        lights_json = HueServicesREST.get_lights(bridge, authentication_handler)
        for i in lights_json:
            json = lights_json.get(i)
            light = Light(i, json['name'], json['type'], json['modelid'], json['manufacturername'], json['uniqueid'], json['swversion'])
            lights.append(light)
        return lights

class GroupsInvenctory(GObject.Object):
    __gtype_name__ = 'GroupsInvectory'

    def __init__(self):
        GObject.GObject.__init__(self)

    @staticmethod
    def get_groups(bridge:Bridge, authentication_handler:AuthenticationHandler):
        groups = []
        groups_json = HueServicesREST.get_groups(bridge, authentication_handler)
        for i in groups_json:
            json = groups_json.get(i)
            group = Group(i, json['name'], json['type'])
            groups.append(group)
        return groups

class BridgeInvenctory(GObject.Object):
    __gtype_name__ = 'BridgeInvectory'

    def __init__(self):
        GObject.GObject.__init__(self)

    @staticmethod
    def get_bridges() -> []:
        bridges = []
        listener = PhilipsHueListener()
        if listener.info != None :
            bridges.append(listener.get_bridge())
        return bridges
