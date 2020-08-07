from threading import Thread

import socket
import time
import json

def readDataUDP(udpIP, port):
    
    UDP_IP   = udpIP
    UDP_PORT = port
    
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024) #buffer size is 1024 bytes

        print("Received Message : %s" % data.decode())
        dictData = json.loads(data.decode().replace("'", "\""))
        print(dictData)
        print("IP ADDRESS : %s"% dictData["IP"])
        if dictData["PORT"] == 5000:
            print("5000 Port")
            sendDataUDP(dictData["IP"], 5004)
        elif dictData["PORT"] == 5001:
            print("5001 Port")
            sendDataUDP(dictData["IP"], 5005)


def sendDataUDP(udpIP, port):

    UDP_IP = udpIP
    UDP_PORT = port
    
    MESSAGE = b"Start Script!"
    print("UDP target IP: %s" % UDP_IP)
    print("UDP target port: %s" % UDP_PORT)
    print("message: %s" % MESSAGE)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


def readThreadUDP(ipAddress, portNo):

    udpPortR = Thread(target = readDataUDP, args=[ipAddress, portNo])
    udpPortR.start()

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

def main():
    hostIpAddress = "10.3.141.1"
    readPort1 = 5000
    readPort2 = 5001
    checkInternet()
    readThreadUDP(hostIpAddress,readPort1)
    readThreadUDP(hostIpAddress,readPort2)

main()
