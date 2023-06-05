import network
import socket
from time import sleep
import machine


ssid = "" #input network/hotspot name
password = "" #input network/hotspot password
def wConnect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print("Waiting for connection")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    #return ip
    
try:
    wConnect()
except KeyboardInterrupt:
    machine.reset()