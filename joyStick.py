#!/usr/bin/python3

import time
import sys
import select
import json
from sense_emu import SenseHat
from time import sleep

sense = SenseHat()

dict_data = {'counter_x':'','counter_y':'', 'counter_middle':'' }

i = ''
timeout = 0.1
counter_middle = 0
counter_x = 0
counter_y = 0

def move(event):
    global counter_x, counter_y, counter_middle
    if event.action in ('pressed'):
        if format(event.direction) == 'left':
            counter_x -= 1
        elif format(event.direction) == 'right':
            counter_x += 1
        elif format(event.direction) == 'up':
            counter_y += 1
        elif format(event.direction) == 'down':
            counter_y -= 1
        elif format(event.direction) == 'middle':
            counter_middle += 1 


print('(--------------------Press ENTER to exit.---------------------)')

while not i: 
    i , o , e = select.select([ sys.stdin ] , [] , [] , timeout)
    
    if (i):
        sys.stdin.readline();
        exit()
        
    for event in sense.stick.get_events():
        if event.action in ('pressed'):
            move(event)
            dict_data['counter_x'] = counter_x
            dict_data['counter_y'] = counter_y
            dict_data['counter_middle'] = counter_middle
            result = json.dumps(dict_data)
            res = '{"Joy-stick":' + result + '}'
            print(res)
            sleep(0.1)

            file = open("/home/pi/sense_hat_api/raport03/joy-stick.dat", "w")
            if file.writable():    
                file.write(res)
            file.close()