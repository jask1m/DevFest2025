from scapy.layers.inet import IP, TCP
from scapy.all import send, get_if_addr, conf
import random
import time

# Get your local IP address (assumes single interface, adjust if needed)
default_iface = conf.iface  # Auto-detect active interface
my_ip = get_if_addr(default_iface)  # Get your machine's IP on that interface

# Define the target IP (simulate a local network or use an external server)
target_ip = my_ip  # Use any IP for target, replace with actual if needed

# Define the destination port (MySQL is typically 3306)
dport = 3306

# Simulate a series of TCP packets (SYN, SYN-ACK, ACK, Data)
seq = random.randint(1000, 2000)  # Randomize sequence number for variety
ack = random.randint(3000, 4000)  # Randomize acknowledgment number for variety

# Step 1: SYN packet (Initial connection request)
syn_packet = IP(dst=target_ip) / TCP(dport=dport, flags="S", seq=seq)
send(syn_packet)

time.sleep(1)  # Add delay to simulate real traffic behavior

# Step 2: SYN-ACK packet (Simulate server response)
syn_ack_packet = IP(dst=target_ip) / TCP(
    dport=dport, flags="SA", seq=seq + 1, ack=seq + 1
)
send(syn_ack_packet)

time.sleep(1)

# Step 3: ACK packet (Client acknowledges the server's response)
ack_packet = IP(dst=target_ip) / TCP(dport=dport, flags="A", seq=seq + 1, ack=ack + 1)
send(ack_packet)

time.sleep(1)

# Step 4: Simulate some data transfer (e.g., simulate a query being sent)
data_packet = (
    IP(dst=target_ip)
    / TCP(dport=dport, flags="PA", seq=seq + 1, ack=ack + 1)
    / b"SELECT * FROM users;"
)
send(data_packet)

print("Simulated traffic sent!")
