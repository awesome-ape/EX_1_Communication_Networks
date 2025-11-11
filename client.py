import socket
import sys
if(len(sys.argv)!=3):
    print("Usage: [serverIP] [serverPort]")
serverIP=sys.argv[1]
serverPort=int(sys.argv[2])
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
domain=input("Enter domain")
s.sendto(domain.encode(), (serverIP, serverPort))
response, addr=s.recvfrom(1024)
print(response.decode())
s.close()
