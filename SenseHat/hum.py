#!/usr/bin/python3

import json
from sense_emu import SenseHat

sense = SenseHat()

# data dictionary
dict_data = {}

humidity_per = sense.humidity
dict_data['name'] = 'humidity'
dict_data['value'] = humidity_per
dict_data['unit'] = '%'
hum = dict_data
hum_json = json.dumps(hum) 

print(hum_json)