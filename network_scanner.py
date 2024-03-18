import scapy.all as scapy
import optparse

def get_argument():
    parser = optparse.OptionParser()
    parser.add_option("-r", "--range", dest="network_ip", help="to enter ip or network range")
    options, arguments = parser.parse_args()

    if not options.network_ip:
        parser.error("[-] Please Specify IP address, -h for help")
    return options


def scan(network_ip):
    arp_req = scapy.ARP(pdst=network_ip)
    arp_broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = arp_broadcast/arp_req
    answer = scapy.srp(arp_req_broadcast, timeout=1, verbose=False)[0]
    client_list=[]

    for ans in answer:
        client_dect={"ip":ans[1].psrc , "mac":ans[1].hwsrc}
        client_list.append(client_dect)
    return client_list

def display_client(client):
    print("IP ADDRESS \t\t MAC Address")
    print("-"*42)
    for client in client_list:
        print(client["ip"],"\t\t" ,client["mac"])

options = get_argument()
client_list=scan(options.network_ip)
display_client(client_list)
