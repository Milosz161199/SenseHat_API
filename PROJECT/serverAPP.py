#!/usr/bin/python3
# File name   : serverAPP.py
# Description : Android App
# Author      : Miłosz Plutowski
# Date        : 2021/04/22


import json
import time
from time import sleep
from sense_hat import SenseHat
import time
from time import ctime
import socket
import random as rnd
import threading

sense = SenseHat()


# data dictionary
dict_data = {'name':'', 'value':'', 'unit':'', 'sensor':''}
dict_data_joy_stick = {'counter_x':'','counter_y':'', 'counter_middle':'' }

timeout = 0.1
counter_middle = 0
counter_x = 10
counter_y = 20


HOST = ''
PORT = 21567
BUFSIZE = 4096

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (HOST, PORT)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)


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


def joy_control():
    while True:
        #print("Watek 1")
        for event in sense.stick.get_events():
            if event.action in ('pressed'):
                
                move(event)
                dict_data_joy_stick['counter_x'] = counter_x
                dict_data_joy_stick['counter_y'] = counter_y
                dict_data_joy_stick['counter_middle'] = counter_middle
                result_joy = json.dumps(dict_data_joy_stick)
                print(result_joy)
                sleep(0.1)

                try:
                    file_joy = open('joy_stick_test_file.json', 'w')
                    if file_joy.writable():    
                        file_joy.write(result_joy)
                except:
                    print('Write Error - JOY')
                finally:
                    file_joy.close()


def serverApp():
    while True:

        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()

        
        try:
        
            print('connection from', client_address)
            
            while True:
                cmd = connection.recv(BUFSIZE)
                cmd = str(cmd, 'utf-8')
                print(cmd)
                
                if cmd == 'get_env_1':
                    t = sense.get_temperature()
                    p = sense.get_pressure()
                    h = sense.get_humidity()
                    data = ('[{"name":"temperature","value":' + str(t) + ',"unit":"C"},' + 
                             '{"name":"pressure","value":' + str(p) + ',"unit":"hPa"},'  +
                             '{"name":"tmpidity","value":' + str(h) + ',"unit":"%"}}]')
                             
                    #save to file
                    try:
                        file = open("envdata.json","w")
                        file.write(data)
                    except:
                        print("Write Error - ENV")
                    finally:
                        file.close()
                if cmd == 'get_env_2':
                    t = sense.get_temperature()
                    p = sense.get_pressure()
                    h = sense.get_humidity()
                    data = ('[{"name":"temperature","value":' + str(32.0 + (9.0 / 5.0) * t) + ',"unit":"F"},' + 
                             '{"name":"pressure","value":' + str(round(p * 0.7500616 , 2)) + ',"unit":"mmHg"},'  +
                             '{"name":"humidity","value":' + str(round(h*100.0, 2)) + ',"unit":"[-]"}]')
                             
                    #save to file
                    try:
                        file = open("envdata.json","w")
                        file.write(data)
                    except:
                        print("Write Error - ENV")
                    finally:
                        file.close() 
                    
                    if cmd == 'get_rpy_deg':
                        sense.set_imu_config(False, True, False)  #  gyroscope enabled
                        orientation_deg = sense.get_orientation_degrees()
                        roll = orientation_deg['roll']
                        pitch = orientation_deg['pitch']
                        yaw = orientation_deg['yaw']

                        data = ('[{"name":"roll","value":' + str(roll) + ',"unit":"deg"},' + 
                                 '{"name":"pitch","value":' + str(pitch) + ',"unit":"deg"},'  +
                                 '{"name":"yaw","value":' + str(yaw) + ',"unit":"deg"}}]')
                                 
                        #save to file
                        try:
                            file = open("rpydata.json","w")
                            file.write(data)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_rpy_rad':
                        sense.set_imu_config(False, True, False)  #  gyroscope enabled
                        orientation_rad = sense.get_orientation_radians()
                        roll = orientation_rad['roll']
                        pitch = orientation_rad['pitch']
                        yaw = orientation_rad['yaw']

                        data = ('[{"name":"roll","value":' + str(roll) + ',"unit":"rad"},' + 
                                 '{"name":"pitch","value":' + str(pitch) + ',"unit":"rad"},'  +
                                 '{"name":"yaw","value":' + str(yaw) + ',"unit":"rad"}}]')
                                 
                        #save to file
                        try:
                            file = open("rpydata.json","w")
                            file.write(data)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                            
                    if cmd == 'get_hum_p':
                        dict_data['name'] = 'humidity'
                        dict_data['value'] = sense.get_tmpidity()
                        dict_data['unit'] = '[%]'
                        dict_data['sensor'] = 'humidity sensor'
                        tmp = dict_data
                        tmp_json = json.dumps(tmp) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_hum_':
                        dict_data['name'] = 'humidity'
                        dict_data['value'] = round(sense.get_tmpidity()/100.0, 2)
                        dict_data['unit'] = '[-]'
                        dict_data['sensor'] = 'humidity sensor'
                        tmp = dict_data
                        tmp_json = json.dumps(tmp) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_temp_C_1':
                        dict_data['name'] = 'temperature'
                        dict_data['value'] = sense.get_temperature()
                        dict_data['unit'] = '[C]'
                        dict_data['sensor'] = 'temperature sensor'
                        tmp = dict_data
                        tmp_json = json.dumps(tmp)
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_temp_C_2':
                        dict_data['name'] = 'temperature'
                        dict_data['value'] = sense.get_temperature_from_humidity()
                        dict_data['unit'] = '[C]'
                        dict_data['sensor'] = 'humidity sensor'
                        tmp = dict_data
                        tmp_json = json.dumps(tmp) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_temp_C_3':
                        dict_data['name'] = 'temperature'
                        dict_data['value'] = sense.get_temperature_from_pressure()
                        dict_data['unit'] = '[C]'
                        dict_data['sensor'] = 'pressure sensor'
                        tmp = dict_data
                        tmp_json = json.dumps(tmp)
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_temp_F_1':
                        dict_data['name'] = 'temperature'
                        dict_data['value'] = 32.0 + (9.0 / 5.0) * sense.get_temperature()
                        dict_data['unit'] = '[F]'
                        dict_data['sensor'] = 'temperature sensor'
                        tmp = dict_data
                        tmp_json = json.dumps(tmp)
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_temp_F_2':
                        dict_data['name'] = 'temperature'
                        dict_data['value'] = 32.0 + (9.0 / 5.0) * sense.get_temperature_from_humidity()
                        dict_data['unit'] = '[F]'
                        dict_data['sensor'] = 'humidity sensor'
                        tmp = dict_data
                        tmp_json = json.dumps(tmp)
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_temp_F_3':
                        dict_data['name'] = 'temperature'
                        dict_data['value'] = 32.0 + (9.0 / 5.0) * sense.get_temperature_from_pressure()
                        dict_data['unit'] = '[F]'
                        dict_data['sensor'] = 'pressure sensor'
                        tmp = dict_data
                        tmp_json = json.dumps(tmp) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_pres_hpa':
                        dict_data['name'] = 'pressure'
                        dict_data['value'] = sense.get_pressure()
                        dict_data['unit'] = '[hPa]'
                        dict_data['sensor'] = 'pressure sensor'
                        tmp = dict_data
                        tmp_json = json.dumps(tmp) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_pres_mm_hg':
                        dict_data['name'] = 'pressure'
                        dict_data['value'] = round(sense.get_pressure() * 0.7500616 , 4)
                        dict_data['unit'] = '[mmHg]'
                        dict_data['sensor'] = 'pressure sensor'
                        tmp = dict_data
                        tmp_json = json.dumps(tmp) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_roll_deg':
                        sense.set_imu_config(False, True, False)  #  gyroscope enabled
                        orientation_deg = sense.get_orientation_degrees()
                        roll = orientation_deg['roll']
                        dict_data['name'] = 'roll'
                        dict_data['value'] = roll
                        dict_data['unit'] = 'deg'  
                        dict_data['sensor'] = 'gyroscope'  
                        r = dict_data
                        tmp_json = json.dumps(r)
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_roll_rad':
                        sense.set_imu_config(False, True, False)  #  gyroscope enabled
                        orientation_deg = sense.get_orientation_radians()
                        roll = orientation_deg['roll']
                        dict_data['name'] = 'roll'
                        dict_data['value'] = roll
                        dict_data['unit'] = 'rad'  
                        dict_data['sensor'] = 'gyroscope'  
                        r = dict_data
                        tmp_json = json.dumps(r)
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_pitch_deg':
                        sense.set_imu_config(False, True, False)  #  gyroscope enabled
                        orientation_deg = sense.get_orientation_degrees()
                        pitch = orientation_deg['pitch']
                        dict_data['name'] = 'pitch'
                        dict_data['value'] = pitch
                        dict_data['unit'] = 'deg'  
                        dict_data['sensor'] = 'gyroscope'  
                        r = dict_data
                        tmp_json = json.dumps(r)
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_pitch_rad':
                        sense.set_imu_config(False, True, False)  #  gyroscope enabled
                        orientation_deg = sense.get_orientation_radians()
                        pitch = orientation_deg['pitch']
                        dict_data['name'] = 'pitch'
                        dict_data['value'] = pitch
                        dict_data['unit'] = 'rad'  
                        dict_data['sensor'] = 'gyroscope'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()                        
                    if cmd == 'get_yaw_deg':
                        sense.set_imu_config(False, True, False)  #  gyroscope enabled
                        orientation_deg = sense.get_orientation_degrees()
                        yaw = orientation_deg['yaw']
                        dict_data['name'] = 'yaw'
                        dict_data['value'] = yaw
                        dict_data['unit'] = 'deg'  
                        dict_data['sensor'] = 'gyroscope'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_yaw_rad':
                        sense.set_imu_config(False, True, False)  #  gyroscope enabled
                        orientation_deg = sense.get_orientation_radians()
                        yaw = orientation_deg['yaw']
                        dict_data['name'] = 'yaw'
                        dict_data['value'] = yaw
                        dict_data['unit'] = 'rad'  
                        dict_data['sensor'] = 'gyroscope'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_compass_north':
                        sense.set_imu_config(True, False, False)  # compass enabled
                        north = sense.get_compass()
                        dict_data['name'] = 'north'
                        dict_data['value'] = north
                        dict_data['unit'] = 'deg'  
                        dict_data['sensor'] = 'compass'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_compass_x':
                        sense.set_imu_config(True, False, False)  #  compass enabled
                        compass = sense.get_compass_raw()
                        x = compass['x']
                        dict_data['name'] = 'compass_x'
                        dict_data['value'] = x
                        dict_data['unit'] = 'uT'  
                        dict_data['sensor'] = 'magnetometer'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_compass_y':
                        sense.set_imu_config(True, False, False)  #  compass enabled
                        compass = sense.get_compass_raw()
                        y = compass['y']
                        dict_data['name'] = 'compass_y'
                        dict_data['value'] = y
                        dict_data['unit'] = 'uT'  
                        dict_data['sensor'] = 'magnetometer'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_compass_z':
                        sense.set_imu_config(True, False, False)  #  compass enabled
                        compass = sense.get_compass_raw()
                        z = compass['z']
                        dict_data['name'] = 'compass_z'
                        dict_data['value'] = z
                        dict_data['unit'] = 'uT'  
                        dict_data['sensor'] = 'magnetometer'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_gyroscope_roll':
                        sense.set_imu_config(False, True, False)  #  gyroscope enabled
                        compass = sense.get_gyroscope()
                        roll = compass['roll']
                        dict_data['name'] = 'gyroscope_roll'
                        dict_data['value'] = roll
                        dict_data['unit'] = 'deg'  
                        dict_data['sensor'] = 'gyroscope'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_gyroscope_pitch':
                        sense.set_imu_config(False, True, False)  #  gyroscope enabled
                        compass = sense.get_gyroscope()
                        pitch = compass['pitch']
                        dict_data['name'] = 'gyroscope_pitch'
                        dict_data['value'] = pitch
                        dict_data['unit'] = 'deg'  
                        dict_data['sensor'] = 'gyroscope'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_gyroscope_yaw':
                        sense.set_imu_config(False, True, False)  #  gyroscope enabled
                        compass = sense.get_gyroscope()
                        yaw = compass['yaw']
                        dict_data['name'] = 'gyroscope_yaw'
                        dict_data['value'] = yaw
                        dict_data['unit'] = 'deg'  
                        dict_data['sensor'] = 'gyroscope'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_gyroscope_x':
                        sense.set_imu_config(False, True, False)  #  gyroscope enabled
                        compass = sense.get_gyroscope_raw()
                        x = compass['x']
                        dict_data['name'] = 'gyroscope_x'
                        dict_data['value'] = x
                        dict_data['unit'] = 'rad/s'  
                        dict_data['sensor'] = 'gyroscope'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_gyroscope_y':
                        sense.set_imu_config(False, True, False)  #  gyroscope enabled
                        compass = sense.get_gyroscope_raw()
                        y = compass['y']
                        dict_data['name'] = 'gyroscope_y'
                        dict_data['value'] = y
                        dict_data['unit'] = 'rad/s'  
                        dict_data['sensor'] = 'gyroscope'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_gyroscope_z':
                        sense.set_imu_config(False, True, False)  #  gyroscope enabled
                        compass = sense.get_gyroscope_raw()
                        z = compass['z']
                        dict_data['name'] = 'gyroscope_z'
                        dict_data['value'] = z
                        dict_data['unit'] = 'rad/s'  
                        dict_data['sensor'] = 'gyroscope'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_accelerometer_roll':
                        sense.set_imu_config(False, False, True)  #  accelerometer enabled
                        acc = sense.get_accelerometer()
                        x = acc['roll']
                        dict_data['name'] = 'accelerometer_roll'
                        dict_data['value'] = x
                        dict_data['unit'] = 'deg'  
                        dict_data['sensor'] = 'accelerometer'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_accelerometer_pitch':
                        sense.set_imu_config(False, False, True)  #  accelerometer enabled
                        acc = sense.get_accelerometer()
                        y = acc['pitch']
                        dict_data['name'] = 'accelerometer_pitch'
                        dict_data['value'] = y
                        dict_data['unit'] = 'deg'  
                        dict_data['sensor'] = 'accelerometer'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_accelerometer_yaw':
                        acc.set_imu_config(False, False, True)  #  accelerometer enabled
                        compass = sense.get_accelerometer()
                        z = acc['yaw']
                        dict_data['name'] = 'accelerometer_yaw'
                        dict_data['value'] = z
                        dict_data['unit'] = 'deg'  
                        dict_data['sensor'] = 'accelerometer'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_accelerometer_x':
                        sense.set_imu_config(False, False, True)  #  accelerometer enabled
                        acc = sense.get_accelerometer_raw()
                        x = acc['x']
                        dict_data['name'] = 'accelerometer_x'
                        dict_data['value'] = x
                        dict_data['unit'] = 'Gs'  
                        dict_data['sensor'] = 'accelerometer'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_accelerometer_y':
                        sense.set_imu_config(False, False, True)  #  accelerometer enabled
                        acc = sense.get_accelerometer_raw()
                        y = acc['y']
                        dict_data['name'] = 'accelerometer_y'
                        dict_data['value'] = y
                        dict_data['unit'] = 'Gs'  
                        dict_data['sensor'] = 'accelerometer'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                    if cmd == 'get_accelerometer_z':
                        acc.set_imu_config(False, False, True)  #  accelerometer enabled
                        compass = sense.get_accelerometer_raw()
                        z = acc['z']
                        dict_data['name'] = 'accelerometer_z'
                        dict_data['value'] = z
                        dict_data['unit'] = 'Gs'  
                        dict_data['sensor'] = 'accelerometer'  
                        r = dict_data
                        tmp_json = json.dumps(r) 
                        #save to file
                        try:
                            file = open("/OneByOne/TEST_file.json","w")
                            file.write(tmp_json)
                        except:
                            print("Write Error - RPY")
                        finally:
                            file.close()
                        
                        #sense.set_imu_config(True, False, False)  #  compass enabled
                        #sense.set_imu_config(False, True, False)  #  gyroscope enabled
                        #sense.set_imu_config(False, False, True)  #  accelerometer enabled
                else:
                    break
                    
        except KeyboardInterrupt:
            connection.close()
        finally:
            connection.close()
  
 
class Thread_JoyStick(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        joy_control()
 

class Thread_Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        serverApp() 
        
#t1=Thread(target=joy_control) 
#t2=Thread(target=serverApp) 
        
if __name__ == "__main__":
    #serverApp()
    
    Thread_JoyStick().start()
    Thread_Server().start()
    ''' JOY-STICK  '''
    #t1.start()
    ''' SERVER  '''
    #t2.start()