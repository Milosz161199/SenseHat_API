#!/usr/bin/python3

import json
from sense_emu import SenseHat

sense = SenseHat()

# data dictionary
dict_data = {}

tempC = sense.temp
dict_data['name'] = 'temperature'
dict_data['value'] = tempC
dict_data['unit'] = 'C'
temp = dict_data
temp_json = json.dumps(temp)

#t_string = '["name"=>"temperature","value"=>tempC,"unit"=>"C"]'

#print(t_string)
print(temp_json)