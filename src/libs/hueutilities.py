import socket
import sys
import requests

from gi.repository import GObject
from zeroconf import ServiceListener, ServiceBrowser, Zeroconf

class PhilipsHueListener(ServiceListener):

    discovered_bridges = {}

    def __init__(self):
        zeroconf = Zeroconf()
        browser = ServiceBrowser(zeroconf, "_hue._tcp.local.", self)
        while True:
            if len(self.discovered_bridges) > 0: break
        zeroconf.close()

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        self.discovered_bridges.update({ name : zc.get_service_info(type_, name)})
        print(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        self.discovered_bridges[name] = zc.get_service_info(type_, name)
        print(f"Service {name} added")

class HueServicesREST(GObject.Object):
    __gtype_name__ = 'HueServicesREST'

    def __init__(self):
        GObject.GObject.__init__(self)

    @staticmethod
    def pair_with_the_bridge(ip_address:str, device_name:str):
        response = requests.post('http://' + ip_address + '/api', json={"devicetype" : device_name})
        for pairing_info in response.json():
            if 'error' in pairing_info:
                raise Exception(pairing_info['error']['description'])
            if 'success' in pairing_info:
                return pairing_info['success']['username']

    @staticmethod
    def get_config(ip_address, user_name:str):
        response = requests.get('http://' + ip_address + '/api/' + user_name + '/config')
        config = response.json()
        if 'error' in config:
            raise Exception(config['error']['description'])
        else :
            return config

    @staticmethod
    def get_light(ip_address:str, user_name:str, light_id:int):
        response = requests.get('http://' + ip_address + '/api/' + user_name + '/lights/' + light_id)
        light = response.json()
        if 'error' in light:
            raise Exception(light['error'])
        else :
            return light

    @staticmethod
    def get_lights(ip_address:str, user_name:str):
        response = requests.get('http://' + ip_address + '/api/' + user_name + '/lights')
        lights = response.json()
        if 'error' in lights:
            raise Exception(lights['error'])
        else :
            return lights

    @staticmethod
    def get_group(ip_address:str, user_name:str, gropu_id:int):
        response = requests.get('http://' + ip_address + '/api/' + user_name + '/groups/' + gropu_id)
        group = response.json()
        if 'error' in group:
            raise Exception(group['error'])
        else :
            lights = {}
            for gropu_id in group['lights']:
                light = self.get_light(bridge, authentication_handler, gropu_id)
                lights[gropu_id] = light
            group['lights'] = lights
            return group

    @staticmethod
    def get_groups(ip_address:str, user_name:str):
        response = requests.get('http://' + ip_address + '/api/' + user_name + '/groups')
        groups = response.json()
        if 'error' in groups:
            raise Exception(groups['error'])
        else :
            #for index in groups:
                #lights = {}
                #for light_id in groups[index]['lights']:
                #    light = HueServicesREST.get_light(bridge, authentication_handler, light_id)
                #    lights[light_id] = light
            #    groups[index]['lights'] = lights
            return groups

    @staticmethod
    def post_new_group(ip_address:str, user_name:str, name:str, lights:list=None, sensors:list=None, group_type:str="Room", group_class:str=None):
        request = {}
        request["name"] = name
        if lights != None :
            request["lights"] = lights
        if sensors != None :
            request["sensors"] = sensors
        if group_type != None :
            request["type"] = group_type
        if group_class != None :
            request["class"] = group_class
        response = requests.post('http://' + ip_address + '/api/' + user_name + '/groups', json=request)
        for set_group_response in response.json():
            if 'error' in set_group_response:
                raise Exception(set_group_response['error'])
            if 'success' in set_group_response:
                return set_group_response['success']['id']

    @staticmethod
    def put_light_status(ip_address:str, user_name:str, index:int, active:str=None , brightness:int=None, alert:str=None, mode:str=None, reachable:bool=None):
        request = {}
        if active != None :
            request["on"] = active
        if brightness != None :
            request["bri"] = brightness
        if alert != None :
            request["alert"] = alert
        if mode != None :
            request["mode"] = mode
        if reachable != None :
            request["reachable"] = reachable
        response = requests.put('http://' + ip_address + '/api/' + user_name + '/lights/' + index + '/state', json=request)
        for set_light_response in response.json():
            if 'error' in set_light_response:
                raise Exception(set_light_response['error'])
            if 'success' in set_light_response:
                return set_light_response['success']

    @staticmethod
    def put_group(ip_address:str, user_name:str, index:int, name:str=None, lights:list=None, group_class:str=None):
        request = {}
        if name != None :
            request["name"] = name
        if lights != None :
            request["lights"] = lights
        if group_class != None :
            request["class"] = group_class
        response = requests.put('http://' + ip_address + '/api/' + user_name + '/groups/' + index, json=request)
        for set_group_response in response.json():
            if 'error' in set_group_response:
                raise Exception(set_group_response['error'])
            if 'success' in set_group_response:
                print(set_group_response['success'])

    @staticmethod
    def put_light_name(ip_address:str, user_name:str, index:int, name:str):
        request = {}
        request["name"] = name
        response = requests.put('http://' + ip_address + '/api/' + user_name + '/lights/' + index, json=request)
        for put_light_response in response.json():
            if 'error' in put_light_response:
                raise Exception(put_light_response['error'])
            if 'success' in put_light_response:
                print(put_light_response['success'])

    @staticmethod
    def put_group_action(ip_address:str, user_name:str, index:int, active:str=None, brightness:int=None, alert:str=None):
        request = {}
        if active != None :
            request["on"] = active
        if brightness != None :
            request["bri"] = brightness
        if alert != None :
            request["alert"] = alert
        print('Hello')
        response = requests.put('http://' + ip_address + '/api/' + user_name + '/groups/' + index + '/action', json=request)
        for set_group_response in response.json():
            if 'error' in set_group_response:
                raise Exception(set_group_response['error'])
            if 'success' in set_group_response:
                return set_group_response['success']

    @staticmethod
    def delete_group(ip_address:str, user_name:str, index:int):
        response = requests.delete('http://' + ip_address + '/api/' + user_name + '/groups/' + index)
        delete_response = response.json()
        if 'error' in delete_response:
            raise Exception(delete_response['error'])

    @staticmethod
    def delete_light(ip_address:str, user_name:str, light_id:int):
        response = requests.delete('http://' + ip_address + '/api/' + user_name + '/groups/' + light_id)
        delete_response = response.json()
        if 'error' in delete_response:
            raise Exception(delete_response['error'])


