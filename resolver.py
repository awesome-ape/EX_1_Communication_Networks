import socket
import sys
import time
if len(sys.argv) != 5:
    print("Usage: [myPort] [parentIP] [parentPort] [x]")
    sys.exit(1)

myport = int(sys.argv[1]) 
parentIP = sys.argv[2]
parentPort = int(sys.argv[3])
x = int(sys.argv[4])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', myport))
cache={}
#key=domain
# value = (response_string, expiration_time)
# print(f"Resolver running on port {myport}, forwarding to {parentIP}:{parentPort}")

while True:
    # Receive a domain query from the client
    domain_bytes, client_addr = s.recvfrom(1024)
    domain = domain_bytes.decode().strip()
    # print(f"Received query from client: {domain}")
    if domain in cache:
        expire_time, res=cache[domain]
        if(time.time()<expire_time):
            s.sendto(res.encode(), client_addr)
            continue
        else:
            del cache[domain]
    # Send the query to the parent server
    s.sendto(domain.encode(), (parentIP, parentPort))

    # Receive the response from the parent server (can be A or NS record)
    response_bytes, _ = s.recvfrom(1024)
    response = response_bytes.decode()

    if response == "non-existent domain":
        # if domain not found, cache the negative response
        cache[domain] = (time.time() + x, response)
        s.sendto(response.encode(), client_addr)
        # print(f"Sent response to client: {response}")
        continue

    fields = response.split(",")
    domain_name = fields[0]   # The relevant domain
    ip_or_ns = fields[1]      # IP address or NS address
    record_type = fields[2]   #  Record type: A or NS

    # Handle NS records: forward the query to the server specified in the NS record
    while record_type == "NS":
        ip, port = ip_or_ns.split(":")
        port = int(port)
        s.sendto(domain.encode(), (ip, port))
        # debug print
        # print(f"Forwarding NS query '{domain}' to {ip}:{port}")
        # Receive the response from the next server in the chain
        response_bytes, _ = s.recvfrom(1024)
        response = response_bytes.decode()
        if response == "non-existent domain":
        # stop the process if non-existent domain is received
            break
        fields = response.split(",")
        record_type = fields[0]
        ip_or_ns = fields[1]
        domain_name = fields[2]
    # Send the final response back to the client
    cache[domain]=(time.time()+x, response)
    s.sendto(response.encode(), client_addr)
    # print(f"Sent response to client: {response}")
