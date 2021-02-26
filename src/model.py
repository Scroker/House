from gi.repository import GObject

class AuthenticationHandler(GObject.Object):

    def __init__(self, user_name):
        GObject.GObject.__init__(self)
        self.user_name = user_name

class Bridge(GObject.Object):

    def __init__(self, bridge_id, internal_ip_address):
        GObject.GObject.__init__(self)
        self.bridge_id = bridge_id
        self.internal_ip_address = internal_ip_address
