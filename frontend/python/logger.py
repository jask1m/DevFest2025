import sys
from scapy.all import sniff, get_if_addr, conf


def show_packet(packet):
    print(packet.show())
    sys.stdout.flush()


# Get your local IP address (assumes single interface, adjust if needed)
default_iface = conf.iface  # Auto-detect active interface
my_ip = get_if_addr(default_iface)  # Get your machine's IP on that interface

# Construct filter string to capture only incoming traffic
print(my_ip)
filter_str = (
    "(tcp) and ("
    "dst port 3306 or dst port 5432 or dst port 6379 or dst port 27017 or dst port 8080 or dst port 443"
    ") and ("
    f"dst host {my_ip}"  # Only capture packets where your machine is the destination
    ")"
)

count = 0


# Callback function to increment and display count
def count_packets(pkt):
    global count
    count += 1
    print(
        f"Packets captured: {count}", end="\r", flush=True
    )  # Overwrites the same line


# Start sniffing
sniff(filter=filter_str, prn=count_packets, store=0)
