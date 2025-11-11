import socket
dns_table = {
    "biu.ac.il": ("biu.ac.il", "1.2.3.4", "A"),
    "example.com": ("example.com", "1.2.3.7", "A"),
    "co.il": ("co.il", "1.2.3.5:777", "NS")
}

SERVER_IP = "0.0.0.0"   
SERVER_PORT = 8053      

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))

print(f"DNS Parent Server is running on port {SERVER_PORT}...")

while True:
    data, addr = server_socket.recvfrom(1024)
    domain = data.decode().strip()
    print(f"Received query for: {domain} from {addr}")

    response = "domain non-existent"  
    for key, record in dns_table.items():
        if record[2] == "A" and domain == record[0]:
            response = f"{record[2]},{record[1]},{record[0]}"
            break
        elif record[2] == "NS" and domain.endswith(record[0]):
            response = f"{record[2]},{record[1]},{record[0]}"
            break

    server_socket.sendto(response.encode(), addr)
    print(f"Sent response: {response}\n")
