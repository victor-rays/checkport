# Checkport

This is a simple application I made for [NextcloudPi](https://github.com/nextcloud/nextcloudpi).

It checks if the port-forwarding has been done properly by trying to open a TCP socket connection to port `80` & `443` on the client IP that is sending a GET request to the `/check` endpoint.

I've used [Sanic](https://sanic.dev/en/) webserver and the Python [Socket](https://docs.python.org/3/library/socket.html) low-level library to reduce the data usage for each request as much as possible.
