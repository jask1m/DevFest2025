import sys
from scapy.all import sniff


def show_packet(packet):
    print(packet.show())
    sys.stdout.flush()


sniff(prn=show_packet, store=0)
