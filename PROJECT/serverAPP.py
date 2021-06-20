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
dict_data = {}
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
                
                if cmd == 'get_env':
                    t = sense.get_temperature()
                    p = sense.get_pressure()
                    h = sense.get_humidity()
                    data = ('[{"name":"temperature","value":' + str(t) + ',"unit":"C"},' + 
                             '{"name":"pressure","value":' + str(p) + ',"unit":"hPa"},'  +
                             '{"name":"humidity","value":' + str(h) + ',"unit":"%"},' +
                             '{"name":"random","value":' + str(rnd.random()) + ',"unit":"-"}]')
                             
                    #save to file
                    try:
                        datafile = open("envdata.json","w")
                        datafile.write(data)
                    except:
                        print("Write Error - ENV")
                    finally:
                        datafile.close()
                        
                    #msg = data.encode('utf-8')
                    #tcpCliSock.sendall(msg)
                    
                    if cmd == 'get_rpy':
                        t = sense.get_temperature()
                        p = sense.get_pressure()
                        h = sense.get_humidity()
                        data = ('[{"name":"temperature","value":' + str(t) + ',"unit":"C"},' + 
                                 '{"name":"pressure","value":' + str(p) + ',"unit":"hPa"},'  +
                                 '{"name":"humidity","value":' + str(h) + ',"unit":"%"},' +
                                 '{"name":"random","value":' + str(rnd.random()) + ',"unit":"-"}]')
                                 
                        #save to file
                        try:
                            datafile = open("rpydata.json","w")
                            datafile.write(data)
                        except:
                            print("Write Error - RPY")
                        finally:
                            datafile.close()
                            
                        #msg = data.encode('utf-8')
                        #tcpCliSock.sendall(msg)   
                else:
                    break
                    
        except KeyboardInterrupt:
            connection.close()
        finally:
            connection.close()
  
 
class Watek_Joy(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        joy_control()
 

class Watek_Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        serverApp() 
        
#t1=Thread(target=joy_control) 
#t2=Thread(target=serverApp) 
        
if __name__ == "__main__":
    #serverApp()
    
    Watek_Joy().start()
    Watek_Server().start()
    ''' JOY-STICK  '''
    #t1.start()
    ''' SERVER  '''
    #t2.start()