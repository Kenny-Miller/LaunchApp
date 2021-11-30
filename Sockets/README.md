# Overview
The purpose of these files is create and setup a simple multi-client/server connection that allows
a user to broadcast commands to connected clients

## SimpleClient Setup Guide
SimpleClient is a sort of dumb client that simply connects to a specified server and then waits to
recieve commands from it. Setting up the connection is simple. On each device that you want a client to run on use: 
> $ python simpleclient.py  addr=<> port<> type=<left|middle|right>

Addr defines what address the server is running on. \
Port defines what port the server on. \
Type defines what wall the client is running on. 

## UserClient Setup Guide
UserClient is a client connection to a server that allows the user to send commands to the server
To setup the connection run the following command on the devices you want to send commands from: 
> $ python usereclient.py  addr=<> port<> 

Addr defines what address the server is running on. \
Port defines what port the server on.

## Server Setup Guide
Server is a server that recieves messages from a userclient, reads them, then broadcasts them to the
appropriate simpleclients. To setup the server run the following command on the device you want the server to run on: 
> $ python server.py  addr=<> port<> 

Addr defines what address the server is running on. \
Port defines what port the server on. 

