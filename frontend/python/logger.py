import sys
from scapy.all import sniff, get_if_addr, conf


def show_packet(packet):
    packet_data = packet.show(dump=True)  # Convert packet to a string representation

    # Assuming you're using a method to send this to Electron via ipcRenderer
    print(packet_data)
    sys.stdout.flush()


# Get your local IP address (assumes single interface, adjust if needed)
default_iface = conf.iface  # Auto-detect active interface
my_ip = get_if_addr(default_iface)  # Get your machine's IP on that interface

# Construct filter string to capture only incoming traffic
print(my_ip)
# filter_str = (
#     "(tcp) and ("
#     "dst port 3306 or dst port 5432 or dst port 6379 or dst port 27017 or dst port 8080 or dst port 443"
#     ") and ("
#     f"dst host {my_ip}"  # Only capture packets where your machine is the destination
#     ")"
# )
filter_str = sys.argv[1]
# filter_str += f" and (dst host {my_ip})"
print(filter_str)
# count = 0
#
#
# # Callback function to increment and display count
# def count_packets(pkt):
#     global count
#     count += 1
#     print(
#         f"Packets captured: {count}", end="\r", flush=True
#     )  # Overwrites the same line
#

# Start sniffing
try:
    sniff(filter=filter_str, prn=show_packet, store=0)
except Exception as e:
    print(filter_str)
    print(e)
