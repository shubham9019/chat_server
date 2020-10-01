from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

cle_ad = ""
# incoming


def incoming():
    while True:
        global cle_ad
        client, client_address = SERVER.accept()
        print("%s:%s Connected" % client_address)
        cle_ad = client_address
        client.send(bytes("Enter Your Nickname:", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    try:
        """Handles a single client connection."""
        name = client.recv(1024).decode("utf8")
        welcome = 'Welcome %s! Type {quit} to exit the chat.' % name
        client.send(bytes(welcome, "utf8"))
        msg = "%s joined the chat" % name
        broadcast(bytes(msg, "utf8"))
        clients[client] = name

        while True:
            msg = client.recv(1024)
            if msg != bytes("{quit}", "utf8"):
                broadcast(msg, name + ": ")
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                broadcast(bytes("%s left" % name, "utf8"))
                break
    except:
        print("%s:%s Disconnected" % cle_ad)


def broadcast(msg, prefix=""):  
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = ''
PORT = 33000
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    ACCEPT_THREAD = Thread(target=incoming)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
