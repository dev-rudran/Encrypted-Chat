# Encrypted Chat Application

A secure, terminal-based chat application with end-to-end encryption using **NaCl** (Networking and Cryptography Library). This application supports both **client** and **server** modes, allowing users to securely send and receive messages. All messages are encrypted with a 256-bit encryption key derived from a user-provided passphrase.

## Features

- **End-to-End Encryption**: All messages are encrypted using NaCl's `SecretBox`.
- **Password-based Key Generation**: A 256-bit key is derived from a passphrase.
- **Peer-to-Peer Communication**: Messages are sent directly between the client and server with a secure connection.
- **Multithreading**: The server supports multiple clients, each with their own encrypted communication.

## Requirements

- **Python 3.x**
- **Libraries**: `nacl`, `rich`
  
  You can install the required libraries with:

  ```bash
  pip install pynacl rich
  ```

## Setup

### 1. Running the Server

To start the server, execute the script in **server mode**:

```bash
python chat.py
```

Then follow the prompts to enter the desired port number and a secure passphrase (at least 16 characters). The server will listen for incoming client connections and will handle encrypted communication.

```bash
Choose mode:
1. Server
2. Client
Enter choice (1/2): 1
Enter port: 12345
Enter 16+ character passphrase: YourSecurePassphrase
```

### 2. Running the Client

To start the client, execute the script in **client mode**:

```bash
python chat.py
```

Then follow the prompts to enter the server's IP address, port, and a passphrase that matches the one used by the server. Once connected, you can send and receive encrypted messages.

```bash
Choose mode:
1. Server
2. Client
Enter choice (1/2): 2
Enter server IP: 127.0.0.1
Enter port: 12345
Enter 16+ character passphrase: YourSecurePassphrase
```

### 3. Encryption Details

- The key used for encryption is derived from the passphrase using a **SHA-256** hash.
- The message is encrypted with NaCl's `SecretBox`, which uses the derived key and a randomly generated nonce.
- Decryption occurs automatically upon receiving a message, with any errors displayed as a warning.

## Example Use

1. **Start the server** on one machine by entering server mode.
2. **Start the client** on another machine, providing the IP and port of the server.
3. Both users can send and receive encrypted messages securely in real-time.

## Security Considerations

- **Key Management**: Ensure that the passphrase used is kept secure, as it is the basis of encryption.
- **Encryption**: The application uses NaCl's `SecretBox`, which provides authenticated encryption (both confidentiality and integrity).
  
## Troubleshooting

- **Decryption Errors**: If there is a mismatch in keys or an error in the encryption process, the client will display `[Decryption Error]`.
- **Server/Client Disconnect**: If the connection is interrupted or an error occurs, the client or server will exit with an error message.

##
This is a personal project for my own development. It currently envisions a lot which I will be implementing upon learning more and updating the Repo.

## License

This project is open-source and available under the [MIT License](LICENSE).

