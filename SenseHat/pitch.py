#!/usr/bin/python3

import json
from sense_emu import SenseHat

sense = SenseHat()

# data dictionary
dict_data = {}

orientation_deg = sense.get_orientation_degrees()
pitch = orientation_deg['pitch']
dict_data['name'] = 'pitch'
dict_data['value'] = pitch
dict_data['unit'] = 'deg'  
p = dict_data
p_json = json.dumps(p) 

print(p_json)