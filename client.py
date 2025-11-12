import socket
import sys
if(len(sys.argv)!=3):
    print("Usage: [serverIP] [serverPort]")
serverIP=sys.argv[1]
serverPort=int(sys.argv[2])
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
domain=input("Enter domain: ")
s.sendto(domain.encode(), (serverIP, serverPort))
response, addr=s.recvfrom(1024)
if response.decode() == "non-existent domain":
    print(response.decode())
    s.close()
    sys.exit(0)
fields = response.decode().split(",")
print(fields[1])
# print all response- for debugging
# print(response.decode())
s.close()
