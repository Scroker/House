import socket
import sys
import requests

from .model import Bridge

class BrigdeUtilities:

    def discover_bridges(self):
        bridges = []
        response = requests.get('https://discovery.meethue.com/')
        for bridge_info in response.json():
            bridge = Bridge(bridge_info['id'], bridge_info['internalipaddress'])
            bridges.append(bridge)
        return bridges

    def pair_with_the_bridge(self, bridge):
        device_name = socket.gethostname() + '#' + sys.platform
        response = requests.post('http://' + bridge.internalIpAddress + '/api', json={"devicetype" : device_name})
        for pairing_info in response.json():
            if 'error' in pairing_info:
                raise Exception(pairing_info['error']['description'])
            if 'success' in pairing_info:
                return pairing_info['success']['username']

    def get_lights(self, bridge, device_id):
        response = requests.get('http://' + bridge.internalIpAddress + '/api/' + device_id + '/lights')
        lights = response.json()
        if 'error' in lights:
            raise Exception(lights['error']['description'])
        else :
            return lights

    def get_groups(self, bridge, device_id):
        response = requests.get('http://' + bridge.internalIpAddress + '/api/' + device_id + '/groups')
        for groups in response.json():
            if 'error' in groups:
                raise Exception(groups['error']['description'])
            else :
                return groups

    def get_config(self, bridge, device_id):
        response = requests.get('http://' + bridge.internalIpAddress + '/api/' + device_id + '/config')
        config = response.json()
        if 'error' in config:
            raise Exception(config['error']['description'])
        else :
            return config

    def get_schedules(self, bridge, device_id):
        response = requests.get('http://' + bridge.internalIpAddress + '/api/' + device_id + '/schedules')
        for schedules in response.json():
            if 'error' in schedules:
                raise Exception(schedules['error']['description'])
            else :
                return schedules

    def get_scenes(self, bridge, device_id):
        response = requests.get('http://' + bridge.internalIpAddress + '/api/' + device_id + '/scenes')
        for scenes in response.json():
            if 'error' in scenes:
                raise Exception(scenes['error']['description'])
            else :
                return scenes

    def get_sensors(self, bridge, device_id):
        response = requests.get('http://' + bridge.internalIpAddress + '/api/' + device_id + '/sensors')
        for sensors in response.json():
            if 'error' in sensors:
                raise Exception(sensors['error']['description'])
            else :
                return sensors

    def get_rules(self, bridge, device_id):
        response = requests.get('http://' + bridge.internalIpAddress + '/api/' + device_id + '/rules')
        for rules in response.json():
            if 'error' in rules:
                raise Exception(rules['error']['description'])
            else :
                return rules

    def set_light_status(self, bridge, device_id, index, status):
        response = requests.put('http://' + bridge.internalIpAddress + '/api/' + device_id + '/lights/' + index + '/state', json={"on" : status})
        for set_light in response.json():
            if 'error' in set_light:
                raise Exception(set_light['error']['description'])
            if 'success' in set_light:
                return True

    def set_light_brightness(self, bridge, device_id, index, brightness):
        response = requests.put('http://' + bridge.internalIpAddress + '/api/' + device_id + '/lights/' + index + '/state', json={"bri" : brightness})
        for set_light in response.json():
            if 'error' in set_light:
                raise Exception(set_light['error']['description'])
            if 'success' in set_light:
                return True
