#!/usr/bin/python3

import json
from sense_emu import SenseHat

sense = SenseHat()

# data dictionary
dict_data = {}

orientation_deg = sense.get_orientation_degrees()
yaw = orientation_deg['yaw']
dict_data['name'] = 'yaw'
dict_data['value'] = yaw
dict_data['unit'] = 'deg'  
y = dict_data
y_json = json.dumps(y) 

print(y_json)