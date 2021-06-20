#!/usr/bin/python3

import json
from sense_emu import SenseHat

sense = SenseHat()

# data dictionary
dict_data = {}


orientation_deg = sense.get_orientation_degrees()
roll = orientation_deg['roll']
dict_data['name'] = 'roll'
dict_data['value'] = roll
dict_data['unit'] = 'deg'  
r = dict_data
r_json = json.dumps(r) 

print(r_json)