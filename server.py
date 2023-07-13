#!/usr/bin/env python3
# Victor-ray, S.

from sanic import Sanic
from sanic.response import json
from sanic.response import text
import ipaddress
import socket

app = Sanic("portcheck")
app.config.REAL_IP_HEADER = "Fly-Client-IP"

@app.route('/<path:path>')
async def index(request, path=""):
    return json({"msg": "I'm a teapot"}, 418)

@app.get('/health')
async def health_check(request):
    return json({"msg": "OK"}, 200)

@app.get('/check')
async def check_ports(request):
    headers = request.headers
    clientIP = headers.get("Fly-Client-IP")
    protocol = ("")
    port80 = ("")
    port443 = ("")
    try:
      validate = await validateIP(clientIP)
      if validate == 0:
        result = "valid"
        if await getIPversion(clientIP) == 4:
          protocol = "IPv4"
          port80 = await checkIPv4(clientIP, 80)
          port443 = await checkIPv4(clientIP, 443)
        else:
          protocol = "IPv6"
          port80 = await checkIPv6(clientIP, 80)
          port443 = await checkIPv6(clientIP, 443)
      elif validate == 1:
        result = "invalid"
      else:
        result = "error"
    except:
      result = "error"
    return json({
      "ip": clientIP,
      "format": result,
      "type": protocol,
      "80": port80,
      "443": port443
    })

@app.get('/80')
async def check_port_80(request):
    headers = request.headers
    clientIP = headers.get("Fly-Client-IP")
    protocol = ("")
    port80 = ("")
    port443 = ("")
    try:
      validate = await validateIP(clientIP)
      if validate == 0:
        result = "valid"
        if await getIPversion(clientIP) == 4:
          protocol = "IPv4"
          port80 = await checkIPv4(clientIP, 80)
        else:
          protocol = "IPv6"
          port80 = await checkIPv6(clientIP, 80)
      elif validate == 1:
        result = "invalid"
      else:
        result = "error"
    except:
      result = "error"
    return json({
      "ip": clientIP,
      "format": result,
      "type": protocol,
      "80": port80
    })

@app.get('/443')
async def check_port_443(request):
    headers = request.headers
    clientIP = headers.get("Fly-Client-IP")
    protocol = ("")
    port80 = ("")
    port443 = ("")
    try:
      validate = await validateIP(clientIP)
      if validate == 0:
        result = "valid"
        if await getIPversion(clientIP) == 4:
          protocol = "IPv4"
          port443 = await checkIPv4(clientIP, 443)
        else:
          protocol = "IPv6"
          port80 = await checkIPv6(clientIP, 443)
      elif validate == 1:
        result = "invalid"
      else:
        result = "error"
    except:
      result = "error"
    return json({
      "ip": clientIP,
      "format": result,
      "type": protocol,
      "443": port443
    })

@app.get('/client')
async def get_client_ip(request):
    try:
      headers = request.headers
      clientIP = headers.get("Fly-Client-IP")
      message = json({"ip":clientIP})
    except:
      message = json({"message":"error"})
    return message

async def validateIP(incomingIP):
    try:
      ip = ipaddress.ip_address(incomingIP)
      validation = 0
    except ValueError:
      validation = 1
    except:
      validation = -1
    return validation

async def getIPversion(theIP):
    try:
      ip = ipaddress.ip_address(theIP)
      if isinstance(ip, ipaddress.IPv4Address):
        protocol = 4
      elif isinstance(ip, ipaddress.IPv6Address):
        protocol = 6
    except:
      protocol = "error"
    return protocol

async def checkIPv4(IPv4, portIPv4):
    try:
      IPv4socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      IPv4socket.settimeout(1.5)
      IPv4socket.connect((IPv4,int(portIPv4)))
      result = "open"
    except:
      result = "closed"
    finally:
      IPv4socket.close()
    return result

async def checkIPv6(IPv6, portIPv6):
    try:
      IPv6socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
      IPv6socket.settimeout(1.5)
      IPv6socket.connect((IPv6,int(portIPv6)))
      result = "open"
    except:
      result = "closed"
    finally:
      IPv6socket.close()
    return result

if __name__ == "__main__":
  app.run(host='::',port=8080,fast=True)
