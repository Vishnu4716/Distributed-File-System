import requests

def put_file(server_host, server_port, filename, content):
    url = f"http://{server_host}:{server_port}/put"
    response = requests.post(url, data={'filename': filename, 'content': content})
    print(response.json())

def get_file(server_host, server_port, filename):
    url = f"http://{server_host}:{server_port}/get"
    response = requests.get(url, params={'filename': filename})
    if response.status_code == 200:
        print(response.json()['content'])
    else:
        print(response.json()['message'])

if __name__ == "__main__":
    server_host = "127.0.0.1"
    server_port = 5000
    
    put_file(server_host, server_port, "example.txt", "This is a test file.")
    get_file(server_host, server_port, "example.txt")
