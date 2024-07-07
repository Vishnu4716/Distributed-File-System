import socket
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

class FileServer:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        print(f"Server started at {host}:{port}")
        self.files = {}

    def handle_client(self, client_socket):
        request = client_socket.recv(1024).decode()
        command, filename, *content = request.split()
        if command == 'PUT':
            self.files[filename] = ' '.join(content)
            client_socket.send(f"File {filename} stored.".encode())
        elif command == 'GET':
            if filename in self.files:
                client_socket.send(self.files[filename].encode())
            else:
                client_socket.send("File not found.".encode())
        client_socket.close()

    def start(self):
        while True:
            client_socket, addr = self.server.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

file_server = FileServer("0.0.0.0", 9999)
threading.Thread(target=file_server.start).start()

@app.route('/put', methods=['POST'])
def put_file():
    filename = request.form['filename']
    content = request.form['content']
    file_server.files[filename] = content
    return jsonify({"message": f"File {filename} stored."})

@app.route('/get', methods=['GET'])
def get_file():
    filename = request.args.get('filename')
    if filename in file_server.files:
        return jsonify({"content": file_server.files[filename]})
    else:
        return jsonify({"message": "File not found."}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
