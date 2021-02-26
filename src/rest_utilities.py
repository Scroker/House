import socket
import sys
import requests

from gi.repository import GObject
from .model import Bridge

class RESTUtilities(GObject.Object):

    def __init__(self):
        GObject.GObject.__init__(self)

    def discover_bridges(self):
        bridges = []
        response = requests.get('https://discovery.meethue.com/')
        for bridge_info in response.json():
            bridge = Bridge(bridge_info['id'], bridge_info['internalipaddress'])
            bridges.append(bridge)
        return bridges

    def pair_with_the_bridge(self, bridge, device_name):
        response = requests.post('http://' + bridge.internal_ip_address + '/api', json={"devicetype" : device_name})
        for pairing_info in response.json():
            if 'error' in pairing_info:
                raise Exception(pairing_info['error'])
            if 'success' in pairing_info:
                authentication_handler = AuthenticationHandler()
                authentication_handler.user_name = pairing_info['success']['username']
                return authentication_handler

    def get_config(self, bridge, authentication_handler):
        response = requests.get('http://' + bridge.internal_ip_address + '/api/' + authentication_handler.user_name + '/config')
        config = response.json()
        if 'error' in config:
            raise Exception(config['error'])
        else :
            return config

    def get_light(self, bridge, authentication_handler, index):
        response = requests.get('http://' + bridge.internal_ip_address + '/api/' + authentication_handler.user_name + '/lights/' + index)
        light = response.json()
        if 'error' in light:
            raise Exception(light['error'])
        else :
            return light

    def get_lights(self, bridge, authentication_handler):
        response = requests.get('http://' + bridge.internal_ip_address + '/api/' + authentication_handler.user_name + '/lights')
        lights = response.json()
        if 'error' in lights:
            raise Exception(lights['error'])
        else :
            return lights

    def get_group(self, bridge, authentication_handler, index):
        response = requests.get('http://' + bridge.internal_ip_address + '/api/' + authentication_handler.user_name + '/groups/' + index)
        group = response.json()
        if 'error' in group:
            raise Exception(group['error'])
        else :
            lights = {}
            for light_id in group['lights']:
                light = self.get_light(bridge, authentication_handler, light_id)
                lights[light_id] = light
            group['lights'] = lights
            return groups

    def get_groups(self, bridge, authentication_handler):
        response = requests.get('http://' + bridge.internal_ip_address + '/api/' + authentication_handler.user_name + '/groups')
        groups = response.json()
        if 'error' in groups:
            raise Exception(groups['error'])
        else :
            for index in groups:
                lights = {}
                for light_id in groups[index]['lights']:
                    light = self.get_light(bridge, authentication_handler, light_id)
                    lights[light_id] = light
                groups[index]['lights'] = lights
            return groups

    def post_new_group(self, bridge, authentication_handler, index, name:str=None, lights:list=None, sensors:list=None, group_type:str=None, group_class:str=None):
        request = {}
        if name != None :
            request["name"] = name
        if lights != None :
            request["lights"] = lights
        if sensors != None :
            request["sensors"] = sensors
        if group_type != None :
            request["type"] = group_type
        if group_class != None :
            request["class"] = group_class
        response = requests.post('http://' + bridge.internal_ip_address + '/api/' + authentication_handler.user_name + '/lights/' + index + '/state', json=request)
        for set_group_response in response.json():
            if 'error' in set_group_response:
                raise Exception(set_group_response['error'])
            if 'success' in set_group_response:
                return set_group_response['success']['id']

    def put_light_status(self, bridge, authentication_handler, index, active:str=None , brightness:int=None, alert:str=None, mode:str=None, reachable:bool=None):
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
        response = requests.put('http://' + bridge.internal_ip_address + '/api/' + authentication_handler.user_name + '/lights/' + index + '/state', json=request)
        for set_light_response in response.json():
            if 'error' in set_light_response:
                raise Exception(set_light_response['error'])
            if 'success' in set_light_response:
                return set_light_response['success']

    def put_group_action(self, bridge, authentication_handler, index, active:str=None, brightness:int=None, alert:str=None):
        request = {}
        if active != None :
            request["on"] = active
        if brightness != None :
            request["bri"] = brightness
        if alert != None :
            request["alert"] = alert
        response = requests.put('http://' + bridge.internal_ip_address + '/api/' + authentication_handler.user_name + '/groups/' + index + '/action', json=request)
        for set_group_response in response.json():
            if 'error' in set_group_response:
                raise Exception(set_group_response['error'])
            if 'success' in set_group_response:
                return set_group_response['success']

