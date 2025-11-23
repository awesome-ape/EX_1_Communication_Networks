import socket
dns_table = {
    "shop.co.il": ("shop.co.il", "10.0.0.10", "A"),
    "news.co.il": ("news.co.il", "10.0.0.11", "A"),
}

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8077 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

print(f"Child DNS Server for co.il is running on port {SERVER_PORT}...")

while True:
    data, addr = server_socket.recvfrom(1024)
    domain = data.decode().strip()
    print(f"Received query for: {domain} from {addr}")

    response = "domain non-existent"
    for key, record in dns_table.items():
        if record[2] == "A" and domain == record[0]:
            response = f"{record[2]},{record[1]},{record[0]}"
            break

    server_socket.sendto(response.encode(), addr)
    print(f"Sent response: {response}\n")