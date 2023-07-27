# Checkport

This is a simple application I made for [NextcloudPi](https://github.com/nextcloud/nextcloudpi).

It checks if the port-forwarding has been done properly and the device is reachable from outside the network.

It does this by trying to open a TCP socket connection to port `80` & `443` on the client IP that is sending a HTTP GET request to the `/check` endpoint of the application.

Returns JSON response body with the following information:
+ **§** `ip`:     Client IP
+ **§** `format`: valid | invalid | error
+ **§** `type`:   IPv4 | IPv6
+ **§** `80`:     open | closed
+ **§** `443`:    open | closed

**§** Clone the repository

```bash
git clone https://github.com/ZendaiOwl/checkport
```

**§** Create a virtual environment with `venv`

```bash
python -m venv venv
```

**§** Activate the virtual environment

```bash
source venv/bin/activate
```

**§** Install `sanic` with

```bash
pip install -r ./requirements.txt
```

**§** Run it locally

I've deployed this app on [fly.io](https://fly.io) so I've changed the app's config for the client IP header to [fly.io](https://fly.io) proxy's header name for the client IP.

It will fall back on the request IP if the proxy header is None, so it should work fine for development locally as is.

Run with

```bash
sanic server:app --dev -p 8080
```

If you omit `-p 8080` it will default to port `8000` when running `sanic` with the `--dev` flag.

Ex. A GET request to the applications `/check` endpoint.

```bash
curl --silent https://localhost:8080/check
```

Receives the following response.

_Note: The IP-address are examples in accordance with [RFC3849][rfc-3849] & [RFC5737][rfc-5737]._

[rfc-3849]: https://datatracker.ietf.org/doc/rfc3849
[rfc-5737]: https://datatracker.ietf.org/doc/rfc5737

+ **§** IPv6

```json
{
  "ip": "2001:DB8::C200:2B46",
  "format": "valid",
  "type": "IPv6",
  "80": "closed",
  "443": "closed"
}
```

+ **§** IPv4

```json
{
  "ip": "192.0.2.12",
  "format": "valid",
  "type": "IPv4",
  "80": "closed",
  "443": "closed"
}
```

You can test it using `netcat`, start a listener on both or one of port `80` & `443`.

_You may need to allow TCP traffic if you have an active firewall blocking incoming traffic_

```bash
sudo nc -l 127.0.0.1 80  # Netcat listens on 127.0.0.1 (localhost) Port 80
sudo nc -l 127.0.0.1 443 # Netcat listens on 127.0.0.1 (localhost) Port 443
```

Send a GET request with `curl` on `localhost` or `127.0.0.1`

```bash
curl -s localhost:8080/80
# Output ↓
{"ip":"127.0.0.1","format":"valid","type":"IPv4","80":"open"}

curl -s localhost:8080/443
# Output ↓
{"ip":"127.0.0.1","format":"valid","type":"IPv4","443":"open"}

curl -s localhost:8080/check # 80 & 443
# Output ↓
{"ip":"127.0.0.1","format":"valid","type":"IPv4","80":"open","443":"open"}
```

I've used [Sanic](https://sanic.dev/en/) webserver and the Python [Socket](https://docs.python.org/3/library/socket.html) low-level library to reduce the data usage for each request as much as possible.

If you want to deploy one yourself as a Docker image you can build one using the Dockerfile, otherwise you need to install the dependencies in the `requirements.txt` file. 

```
# $USERNAME: Username at the Docker Hub image registry
# $REPOSITORY: Repository at the Docker Hub image registry
# $IMAGE_TAG: The tag for the image
docker build . -t "$USERNAME/$REPOSITORY:$IMAGE_TAG"
```

Or if you want to use the one I've built 


```
docker pull zendai/checkport:sanic
docker run --rm --detach --publish 8080:8080 zendai/checkport:sanic
```

