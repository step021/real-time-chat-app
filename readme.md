-  Sebastian Stephens 


- files
- tchatcli.py - Client side script that allows user to connect to server. It allows for all the commands to be sent.
- tchatsrv.py - Server side script for chat app. It handles command parsing, client connection, etc. 
- readme.md - description of project

- Protocol 
- The client initiates a connection to the server's IP address and port. Sends the username followed by a newline character (\n).
-  Client Command: message <hashtag> <message_content>\n
- Client Command: subscribe <hashtag>\n
- Client Command: unsubscribe <hashtag>\n
- Client Command: exit\n
- Servers respondsto all of these with its own response on the server side it also parses these commands. 
- clients_lock: Ensures that modifications to connected_clients are thread-safe.
- subscriptions_lock: Protects access to subscriptions and user_subscriptions.

