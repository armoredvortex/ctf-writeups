#!/usr/bin/env python3
import socket
import threading
import random
import string
import hashlib
from secret import flag,admin_pass
# The flag for the challenge (modify as needed)
FLAG = flag

def generate_salt(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def secret_hash(s, salt):
    return hashlib.sha3_256((s + salt).encode()).hexdigest()

def handle_client(conn, addr):
    try:
        # Each connection gets a new session salt
        session_salt = generate_salt(32)
        admin_password =  admin_pass # The admin password (hidden on the server)
        admin_hash = secret_hash(admin_password, session_salt)
        
        conn.sendall(b"Welcome to the challenge server!\n")
        while True:
            conn.sendall(b">>> ")
            data = conn.recv(1024)
            if not data:
                break
            data = data.strip()
            
            # Vulnerability: if the client sends the special byte 0x7f, leak the admin hash and session salt
            if b'\x7f' in data:
                leak = f"admin: {admin_hash}\nSecret salt: '{session_salt}'\n".encode()
                conn.sendall(leak)
                continue
            
            # Login option
            if data == b'1':
                conn.sendall(b"username: ")
                username = conn.recv(1024).strip().decode()
                if username != "admin":
                    conn.sendall(b"Only admin login is supported.\n")
                    continue
                # For admin login, generate a new login salt
                login_salt = generate_salt(32)
                prompt = f"Compute hash(admin_hash + '{login_salt}'): ".encode()
                conn.sendall(prompt)
                user_hash = conn.recv(1024).strip().decode()
                expected = secret_hash(admin_hash, login_salt)
                if user_hash == expected:
                    conn.sendall(f"Access granted. Flag: {FLAG}\n".encode())
                else:
                    conn.sendall(b"Access denied.\n")
            elif data == b'3':
                conn.sendall(b"Goodbye!\n")
                break
            else:
                conn.sendall(b"Invalid option.\n")
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        conn.close()

def main():
    host = "0.0.0.0"
    port = 7331
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        print(f"Server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            print(f"Connection from {addr}")
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.start()

if __name__ == "__main__":
    main()