from scapy.layers.inet import IP, TCP
from scapy.all import send
from scapy.all import get_if_addr, conf


# Get your local IP address (assumes single interface, adjust if needed)
default_iface = conf.iface  # Auto-detect active interface
my_ip = get_if_addr(default_iface)  # Get your machine's IP on that interface

# Construct an incoming packet to your IP address (simulate MySQL traffic)
packet = IP(dst=my_ip) / TCP(
    dport=3306, flags="S"
)  # SYN flag to simulate a connection request

# Send the packet
send(packet)

print("Simulated packet sent!")
