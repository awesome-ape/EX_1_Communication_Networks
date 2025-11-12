import socket
import sys

def load_zone(file_name):
    zone = {}
    with open(file_name, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                domain, ip, rec_type = line.split(',')
                zone[domain] = (rec_type, ip)
    return zone


def main():
    if len(sys.argv) != 3:
        print("Usage: python server.py [myPort] [zoneFileName]")
        return
    
    port = int(sys.argv[1])
    zone_file = sys.argv[2]
    # load zone file
    zone = load_zone(zone_file)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', port))
    print(f"Server listening on port {port}...")

    while True:
        data, addr = s.recvfrom(1024)
        domain = data.decode().strip()
        response = "non-existent domain"

        # check if domain exists in zone
        if domain in zone:
            rec_type, ip = zone[domain]
            response = f"{rec_type},{ip},{domain}"

        # NS
        # if domain not found, check for NS records for parent domains
        else:
            for z_domain, (rec_type, ip) in zone.items():
                if rec_type == "NS" and domain.endswith(z_domain.strip('.')):
                    response = f"NS,{ip},{z_domain}"
                    break

        s.sendto(response.encode(), addr)

if __name__ == "__main__":
    main()