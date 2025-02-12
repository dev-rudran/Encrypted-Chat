import socket
import threading
import nacl.secret
import nacl.utils
import nacl.encoding
import nacl.hash
import sys
from rich.console import Console
from rich.text import Text

console = Console()

def generate_key(passphrase):
    if len(passphrase) < 16:
        raise ValueError("Passphrase must be at least 16 characters long")
    return nacl.hash.sha256(passphrase.encode(), encoder=nacl.encoding.RawEncoder)[:32]

def encrypt_message(message, key):
    box = nacl.secret.SecretBox(key)
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    encrypted = box.encrypt(message.encode(), nonce)
    return encrypted

def decrypt_message(encrypted, key):
    box = nacl.secret.SecretBox(key)
    try:
        decrypted = box.decrypt(encrypted).decode()
        return decrypted
    except Exception:
        return "[Decryption Error]"

def handle_receive(client_socket, key):
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break
            decrypted_message = decrypt_message(encrypted_message, key)
            console.print(Text(decrypted_message, style="bold yellow"))
        except Exception as e:
            console.print(f"[Error] {e}", style="bold red")
            break

def start_client(ip, port, passphrase):
    key = generate_key(passphrase)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    
    threading.Thread(target=handle_receive, args=(client_socket, key), daemon=True).start()
    console.print("[Connected to chat. Type your messages below]", style="bold green")
    
    try:
        while True:
            message = input().strip()
            if not message:
                continue
            encrypted_message = encrypt_message(message, key)
            client_socket.send(encrypted_message)
    except KeyboardInterrupt:
        console.print("\n[Disconnected]", style="bold red")
    finally:
        client_socket.close()

def start_server(port, passphrase):
    key = generate_key(passphrase)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    console.print(f"[Server started on port {port}. Waiting for connections...]")
    
    clients = []
    clients_lock = threading.Lock()
    
    def handle_client(client_socket):
        while True:
            try:
                encrypted_message = client_socket.recv(1024)
                if not encrypted_message:
                    break
                decrypted_message = decrypt_message(encrypted_message, key)
                console.print(Text(decrypted_message, style="bold yellow"))
                with clients_lock:
                    for client in clients:
                        if client != client_socket:
                            client.send(encrypted_message)
            except Exception:
                break
        client_socket.close()
        with clients_lock:
            if client_socket in clients:
                clients.remove(client_socket)
    
    try:
        while True:
            client_socket, addr = server_socket.accept()
            with clients_lock:
                clients.append(client_socket)
            threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
            console.print(f"[New connection from {addr}]")
    except KeyboardInterrupt:
        console.print("\n[Server shutting down]", style="bold red")
    finally:
        server_socket.close()

if __name__ == "__main__":
    console.print("Choose mode:", style="bold cyan")
    console.print("1. Server", style="bold yellow")
    console.print("2. Client", style="bold yellow")
    
    mode_choice = input("Enter choice (1/2): ").strip()
    if mode_choice == "1":
        mode = "server"
        port = int(input("Enter port: ").strip())
        passphrase = input("Enter 16+ character passphrase: ").strip()
        if len(passphrase) < 16:
            console.print("Passphrase must be at least 16 characters long.", style="bold red")
            sys.exit(1)
        start_server(port, passphrase)
    elif mode_choice == "2":
        mode = "client"
        ip = input("Enter server IP: ").strip()
        port = int(input("Enter port: ").strip())
        passphrase = input("Enter 16+ character passphrase: ").strip()
        if len(passphrase) < 16:
            console.print("Passphrase must be at least 16 characters long.", style="bold red")
            sys.exit(1)
        start_client(ip, port, passphrase)
    else:
        console.print("Invalid choice. Use '1' for server or '2' for client.", style="bold red")
        sys.exit(1)