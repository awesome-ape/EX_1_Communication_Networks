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

# import socket
# import sys

# def load_zone(file_name):
#     zone = {}
#     with open(file_name, 'r') as f:
#         for line in f:
#             line = line.strip()
#             if line:
#                 domain, ip, rec_type = line.split(',')
#                 zone[domain] = (rec_type, ip)
#     return zone


# def main():
#     if len(sys.argv) != 3:
#         print("Usage: python server.py [myPort] [zoneFileName]")
#         return
    
#     port = int(sys.argv[1])
#     zone_file = sys.argv[2]
#     # load zone file
#     zone = load_zone(zone_file)

#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.bind(('', port))
#     print(f"Server listening on port {port}...")

#     while True:
#         data, addr = s.recvfrom(1024)
#         domain = data.decode().strip()
#         response = "non-existent domain"

#         # check if domain exists in zone
#         if domain in zone:
#             rec_type, ip = zone[domain]
#             response = f"{domain},{ip},{rec_type}"

#         # NS
#         # if domain not found, check for NS records for parent domains
#         else:
#             for z_domain, (rec_type, ip) in zone.items():
#                 if rec_type == "NS" and domain.endswith(z_domain.strip('.')):
#                     response = f"{z_domain},{ip},NS"
#                     break

#         s.sendto(response.encode(), addr)

# if __name__ == "__main__":
#     main()