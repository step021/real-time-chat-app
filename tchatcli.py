import socket
import threading
import sys
import time

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 tchatcli.py <serverIP> <serverPort> <username>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    username = sys.argv[3]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
    except:
        print("Connection Failed", flush=True)
        sys.exit(1)

    client_socket.send("{}\n".format(username).encode())
    buffer = ''
    while True:
        data = client_socket.recv(1024)
        if not data:
            print("Connection Failed", flush=True)
            client_socket.close()
            sys.exit(1)
        buffer += data.decode()
        if '\n' in buffer:
            response, buffer = buffer.split('\n', 1)
            response = response.strip()
            break
    if response == "USERNAME_TAKEN":
        print("Connection Failed: Username Taken", flush=True)
        client_socket.close()
        sys.exit(1)
    elif response == "CONNECTED":
        print("Connected to {} on port {}".format(server_ip, server_port), flush=True)
    else:
        print("Connection Failed", flush=True)
        client_socket.close()
        sys.exit(1)

    messages = []
    messages_lock = threading.Lock()

    def receive_messages():
        buffer = ''
        while True:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                buffer += data.decode()
                while '\n' in buffer:
                    message, buffer = buffer.split('\n', 1)
                    message = message.strip()
                    if message.startswith("subscribe:") or message.startswith("unsubscribe:") or message.startswith("Message: Illegal Message") or message.startswith("subscribe: Too many Subscriptions"):
                        print(message, flush=True)
                    elif message.endswith("sent"):
                        print(message, flush=True)
                    else:
                        print(message, flush=True)
                        with messages_lock:
                            messages.append(message)
            except:
                break

    threading.Thread(target=receive_messages, daemon=True).start()

    while True:
        try:
            time.sleep(0.1)  
            command = input(">> ").strip()
            if not command:
                continue
            tokens = command.split()
            cmd = tokens[0]
            if cmd == "message":
                client_socket.send("{}\n".format(command).encode())
            elif cmd == "subscribe":
                client_socket.send("{}\n".format(command).encode())
            elif cmd == "unsubscribe":
                client_socket.send("{}\n".format(command).encode())
            elif cmd == "timeline":
                with messages_lock:
                    if messages:
                        for msg in messages:
                            print(msg, flush=True)
                        messages.clear()
                    else:
                        print("timeline: No Messages Available", flush=True)
            elif cmd == "exit":
                client_socket.send("exit\n".encode())
                client_socket.close()
                sys.exit(0)
            else:
                pass
        except KeyboardInterrupt:
            client_socket.send("exit\n".encode())
            client_socket.close()
            sys.exit(0)
        except:
            pass

if __name__ == "__main__":
    main()
