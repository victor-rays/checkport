# Checkport

This is a simple application I made for [NextcloudPi](https://github.com/nextcloud/nextcloudpi).

It checks if the port-forwarding has been done properly and the device is reachable from outside the network.

It does this by trying to open a TCP socket connection to port `80` & `443` on the client IP that is sending a HTTP GET request to the `/check` endpoint of the application.

Returns JSON response body with the following information:
+ **§** ip:     Client IP
+ **§** format: valid / invalid / error
+ **§** type:   IPv4 / IPv6
+ **§** 80:     open / closed
+ **§** 443:    open / closed

Ex. A HTTP GET request over TCP to the applications '/check' endpoint.

```bash
curl -sL https://checkport.zendai.net.eu.org/check
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

I've used [Sanic](https://sanic.dev/en/) webserver and the Python [Socket](https://docs.python.org/3/library/socket.html) low-level library to reduce the data usage for each request as much as possible.

If you want to deploy one yourself as a Docker image you can build one using the Dockerfile, otherwise you need to install the dependencies in the `requirements.txt` file. 

```
# USERNAME: Username at the Docker Hub image registry
# REPOSITORY: Repository at the Docker Hub image registry
# IMAGE_TAG: The tag for the image
docker build . -t $USERNAME/$REPOSITORY:$IMAGE_TAG
```

```python
pip install -r ./requirements.txt
```
