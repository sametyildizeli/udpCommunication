
################### TITLE : RPi Zero Camera Script #######################
# THIS SCRPIT IS USED FOR VIDEO STREAMING TO THE HUB (A+)
#
# ROLES OF PYTHON SCRIPT OF THE RPi ZERO AS CAMERA:
# * CHECKS THE FOLLOWING LIST THAT WORKS OR NOT:
#       - WIFI CONNECTION
#       - INTERNET CONNECTION
#       - GSTREAMER HAS STARTED OR NOT
#       - RUNS GSTREAMER IF CONNECTIONS (WIFI, INTERNET) HAS NO PROBLEM
#       - CONFIGURATE SCRIPT OF THE GST WITH DYNAMIC IP ADDRESS

import netifaces as ni
import time

def checkIpMacAddress():
    while True:
        try:
            #macAddress = ni.ifaddresses('wlan0')[ni.AF_LINK][0]['addr']    # get MAC Address
            ipAddress  = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']    # get IP Address
        except:
            ipAddress = None

        try:
            macAddress = ni.ifaddresses('wlan0')[ni.AF_LINK][0]['addr']    # get MAC Add$
            #ipAddress  = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']    # get IP Addr$
        except:
            macAddress = None

        print(ipAddress)
        print(macAddress)

        if ipAddress != None and macAddress != None:
            return [ipAddress, macAddress]

        time.sleep(1)

import urllib.request

def checkInternet():
    while True:
        try:
            url = "https://www.google.com"
            urllib.request.urlopen(url)
            status = "Connected"
        except:
            status = "Not Connected"

        print(status)

        if status == "Connected":
            break
        time.sleep(1)

#deviceDict = {"IP": ipAddress, "MAC": macAddress}
#deviceDict = str(deviceDict)

import socket

def sendDataUDP(ipAddress, macAddress):
    UDP_IP = "10.3.141.1" #"127.0.0.1"
    UDP_PORT = 5000

    deviceDict = {"IP": ipAddress, "MAC": macAddress, "PORT": UDP_PORT}
    deviceDict = str(deviceDict)

    #MESSAGE = b"Hello, World!"
    MESSAGE = str.encode(deviceDict)
    print("UDP target IP: %s" % UDP_IP)
    print("UDP target port: %s" % UDP_PORT)
    print("message: %s" % MESSAGE)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

def readDataUDP(ipAddress):
    UDP_IP = ipAddress
    UDP_PORT = 5004
    
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024) #buffer size is 1024 bytes

        print("Received Message : %s" % data.decode())

def main():
    [ipAddress, macAddress] = checkIpMacAddress()
    sendDataUDP(ipAddress,macAddress)
    readDataUDP(ipAddress)


main()
