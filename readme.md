-  Sebastian Stephens 
-  Sstephens42@gatech.edu

- CS 3251, PA2, 11/25/2024

- files
- tchatcli.py - Client side script that allows user to connect to server. It allows for all the commands to be sent.
- tchatsrv.py - Server side script for chat app. It handles command parsing, client connection, etc. 
- readme.md - description of project

- Key learnings
- Through implementing the client server program, I learned more about Pythons socket library and how TCP/IP protocols help network communication.
- By using threading, I was able to handle multiple client messgaes on the server side. 
- threading.Lock() taught me the importance of thread safety when accessing shared resources and preventing race conditions.
- Clear understanding in protocol for sending basic messages in netwroking

- Challenges
- Ensuring that the server could handle multiple clients without conflicts. This was hard as I kept getting bugs 
- Initially, messages sent by a client weren't received by the sender if they were subscribed to the hashtag. I had to fix this in the program and it eventually worked.

- Process
- First i setup client and server, then i established protocols for communication and different commands used. Then i handled edge cases and continued to test for errors. 

- Bugs/Limitations
- No user authentication
- message size restriction
- lack of scalability 

- Protocol 
- The client initiates a connection to the server's IP address and port. Sends the username followed by a newline character (\n).
-  Client Command: message <hashtag> <message_content>\n
- Client Command: subscribe <hashtag>\n
- Client Command: unsubscribe <hashtag>\n
- Client Command: exit\n
- Servers respondsto all of these with its own response on the server side it also parses these commands. 
- clients_lock: Ensures that modifications to connected_clients are thread-safe.
- subscriptions_lock: Protects access to subscriptions and user_subscriptions.

