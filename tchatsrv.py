import socket
import threading
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 tchatsrv.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen()

    print("Server started on port {}. Accepting connections".format(port), flush=True)

    connected_clients = {} 
    subscriptions = {}      
    user_subscriptions = {}
    clients_lock = threading.Lock()
    subscriptions_lock = threading.Lock()

    def handle_client(client_socket):
        try:
            buffer = ''
            while True:
                data = client_socket.recv(1024)
                if not data:
                    client_socket.close()
                    return
                buffer += data.decode()
                if '\n' in buffer:
                    username, buffer = buffer.split('\n', 1)
                    username = username.strip()
                    break
            if not username:
                client_socket.close()
                return

            with clients_lock:
                if username in connected_clients:
                    client_socket.send("USERNAME_TAKEN\n".encode())
                    client_socket.close()
                    return
                else:
                    connected_clients[username] = client_socket
                    print("{} logged in".format(username), flush=True)
                    client_socket.send("CONNECTED\n".encode())

            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                buffer += data.decode()
                while '\n' in buffer:
                    command, buffer = buffer.split('\n', 1)
                    command = command.strip()
                    if not command:
                        continue
                    handle_command(username, command)
        except:
            pass
        finally:
            with clients_lock:
                if username in connected_clients:
                    del connected_clients[username]
                    print("{} logged out".format(username), flush=True)
            with subscriptions_lock:
                if username in user_subscriptions:
                    for hashtag in user_subscriptions[username]:
                        if hashtag in subscriptions and username in subscriptions[hashtag]:
                            subscriptions[hashtag].remove(username)
                            if not subscriptions[hashtag]:
                                del subscriptions[hashtag]
                    del user_subscriptions[username]
            client_socket.close()

    def handle_command(username, command):
        tokens = command.split()
        if not tokens:
            return
        cmd = tokens[0]
        if cmd == "message":
            if len(tokens) >= 3:
                hashtag = tokens[1]
                message = ' '.join(tokens[2:])
                if len(message) < 1 or len(message) > 150:
                    connected_clients[username].send("Message: Illegal Message\n".encode())
                else:
                    confirmation = "{}: {} {} sent\n".format(username, hashtag, message)
                    connected_clients[username].send(confirmation.encode())
                    print("{}: {} {} sent".format(username, hashtag, message), flush=True)
                    message_to_send = "{}: {} {}\n".format(username, hashtag, message)
                    with subscriptions_lock:
                        recipients = set()
                        if hashtag in subscriptions:
                            recipients.update(subscriptions[hashtag])
                        if '#ALL' in subscriptions:
                            recipients.update(subscriptions['#ALL'])
                    if username in user_subscriptions and hashtag in user_subscriptions[username]:
                        recipients.add(username)
                    for recipient_username in recipients:
                        if recipient_username in connected_clients:
                            try:
                                connected_clients[recipient_username].send(message_to_send.encode())
                            except:
                                pass
        elif cmd == "subscribe":
            if len(tokens) == 2:
                hashtag = tokens[1]
                with subscriptions_lock:
                    if username not in user_subscriptions:
                        user_subscriptions[username] = set()
                    if hashtag in user_subscriptions[username]:
                        connected_clients[username].send("subscribe: {} added\n".format(hashtag).encode())
                        print("{}: subscribed {}".format(username, hashtag), flush=True)
                    else:
                        if len(user_subscriptions[username]) >= 5:
                            connected_clients[username].send("subscribe: Too many Subscriptions\n".encode())
                            return
                        user_subscriptions[username].add(hashtag)
                        if hashtag not in subscriptions:
                            subscriptions[hashtag] = set()
                        subscriptions[hashtag].add(username)
                        connected_clients[username].send("subscribe: {} added\n".format(hashtag).encode())
                        print("{}: subscribed {}".format(username, hashtag), flush=True)
        elif cmd == "unsubscribe":
            if len(tokens) == 2:
                hashtag = tokens[1]
                with subscriptions_lock:
                    if username in user_subscriptions and hashtag in user_subscriptions[username]:
                        user_subscriptions[username].remove(hashtag)
                        if hashtag in subscriptions and username in subscriptions[hashtag]:
                            subscriptions[hashtag].remove(username)
                            if not subscriptions[hashtag]:
                                del subscriptions[hashtag]
                    connected_clients[username].send("unsubscribe: {} removed\n".format(hashtag).encode())
                    print("{}: unsubscribed {}".format(username, hashtag), flush=True)
        elif cmd == "exit":
            connected_clients[username].close()
        else:
            pass

    while True:
        client_socket, _ = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    main()
