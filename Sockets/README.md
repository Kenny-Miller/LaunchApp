# Overview
The purpose of these files is create and setup a simple multi-client/server connection that allows
a user to broadcast commands to connected clients
## Setup Guide
#### SimpleClient
SimpleClient is a sort of dumb client that simply connects to a specified server and then waits to
recieve commands from it. Setting up the connection is simple. On each device that you want a client to run on use: 
> $ python simpleclient.py  addr=<> port<> type=<left|middle|right>

Addr defines what address the server is running on. \
Port defines what port the server on. \
Type defines what wall the client is running on. 

#### UserClient
UserClient is a client connection to a server that allows the user to send commands to the server
To setup the connection run the following command on the devices you want to send commands from: 
> $ python usereclient.py  addr=<> port<> 

Addr defines what address the server is running on. \
Port defines what port the server on.

#### Server
Server is a server that recieves messages from a userclient, reads them, then broadcasts them to the
appropriate simpleclients. To setup the server run the following command on the device you want the server to run on: 
> $ python server.py  addr=<> port<> 

Addr defines what address the server is running on. \
Port defines what port the server on. 

## Commands
Currently there are only a handful of commands that will be successfully sent from a userclient
* stop, s | Closes the client connection 
* shutdown, sd | Shuts down the server and closes all client connections
* test | Sends a test message that each client will echo
* vlc | Puts the userclient in vlc mode. See vlc section

### VLC Commands
While in vlc mode:
* load | Loads a media file
* exit | Exits vlc mode and closes the media player on all clients
* play | plays the video on all clients
* pause | pauses the video on all clients
* init | Initializes the videoplayer on all clients. Must be ran before other vlc commands will work