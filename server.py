#!/usr/bin/env python3
# § Victor-ray, S.

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
    client_ip = headers.get("Fly-Client-IP")
    if client_ip is None:
        client_ip = request.ip
    protocol = ("")
    port80 = ("")
    port443 = ("")
    try:
      validate = await validate_ip(client_ip)
      if validate == 0:
        result = "valid"
        if await get_ip_version(client_ip) == 4:
          protocol = "IPv4"
          port80 = await check_ip_v4(client_ip, 80)
          port443 = await check_ip_v4(client_ip, 443)
        else:
          protocol = "IPv6"
          port80 = await check_ip_v6(client_ip, 80)
          port443 = await check_ip_v6(client_ip, 443)
      elif validate == 1:
        result = "invalid"
      else:
        result = "error"
    except:
      result = "error"
    return json({
      "ip": client_ip,
      "format": result,
      "type": protocol,
      "80": port80,
      "443": port443
    }, 200)

@app.get('/80')
async def check_port_80(request):
    headers = request.headers
    client_ip = headers.get("Fly-Client-IP")
    if client_ip is None:
        client_ip = request.ip
    protocol = ("")
    port80 = ("")
    port443 = ("")
    try:
      validate = await validate_ip(client_ip)
      if validate == 0:
        result = "valid"
        if await get_ip_version(client_ip) == 4:
          protocol = "IPv4"
          port80 = await check_ip_v4(client_ip, 80)
        else:
          protocol = "IPv6"
          port80 = await check_ip_v6(client_ip, 80)
      elif validate == 1:
        result = "invalid"
      else:
        result = "error"
    except:
      result = "error"
    return json({
      "ip": client_ip,
      "format": result,
      "type": protocol,
      "80": port80
    }, 200)

@app.get('/443')
async def check_port_443(request):
    headers = request.headers
    client_ip = headers.get("Fly-Client-IP")
    if client_ip is None:
        client_ip = request.ip
    protocol = ("")
    port80 = ("")
    port443 = ("")
    try:
      validate = await validate_ip(client_ip)
      if validate == 0:
        result = "valid"
        if await get_ip_version(client_ip) == 4:
          protocol = "IPv4"
          port443 = await check_ip_v4(client_ip, 443)
        else:
          protocol = "IPv6"
          port80 = await check_ip_v6(client_ip, 443)
      elif validate == 1:
        result = "invalid"
      else:
        result = "error"
    except:
      result = "error"
    return json({
      "ip": client_ip,
      "format": result,
      "type": protocol,
      "443": port443
    }, 200)

@app.get('/client')
async def get_client_ip(request):
    try:
      headers = request.headers
      client_ip = headers.get("Fly-Client-IP")
      if client_ip is None:
        client_ip = request.ip
      message = json({"ip": client_ip})
    except:
      message = json({"message": "error"})
    return message

async def validate_ip(incoming_ip):
    try:
      ip = ipaddress.ip_address(incoming_ip)
      validation = 0
    except ValueError:
      validation = 1
    except:
      validation = -1
    return validation

async def get_ip_version(incoming_ip):
    try:
      ip = ipaddress.ip_address(incoming_ip)
      if isinstance(ip, ipaddress.IPv4Address):
        protocol = 4
      elif isinstance(ip, ipaddress.IPv6Address):
        protocol = 6
    except:
      protocol = "error"
    return protocol

async def check_ip_v4(IPv4, portIPv4):
    try:
      IPv4socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      IPv4socket.settimeout(1.5)
      IPv4socket.connect(( IPv4, int(portIPv4) ))
      result = "open"
    except:
      result = "closed"
    finally:
      IPv4socket.close()
    return result

async def check_ip_v6(IPv6, portIPv6):
    try:
      IPv6socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
      IPv6socket.settimeout(1.5)
      IPv6socket.connect(( IPv6, int(portIPv6) ))
      result = "open"
    except:
      result = "closed"
    finally:
      IPv6socket.close()
    return result

if __name__ == "__main__":
  app.run(
    host='::',
    port=8080,
    fast=True
  )
