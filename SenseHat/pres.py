#!/usr/bin/python3

import json
from sense_emu import SenseHat

sense = SenseHat()

# data dictionary
dict_data = {}

pressure_hpa = sense.pressure
dict_data['name'] = 'pressure'
dict_data['value'] = pressure_hpa
dict_data['unit'] = 'hPa'  
pres = dict_data
pres_json = json.dumps(pres) 

print(pres_json)