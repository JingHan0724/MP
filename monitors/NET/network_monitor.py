from scapy.all import *
import os
import time
import requests

server_url = "https://192.168.1.100:5002/sensor/network"

# Define a packet handler function to append packets to a list
def packet_handler(packet, captured_packets):
    captured_packets.append(packet)

# Function to capture and save network packets
def capture_and_save(networkInterface):
    while True:
        current_timestamp = int(time.time())

        captured_packets = []

        # Capture network traffic for 5 seconds
        sniff(iface=networkInterface, prn=lambda packet: packet_handler(packet, captured_packets), timeout=5)

        # Call render_content_from_pcap to process and send captured packets
        render_content_from_pcap(captured_packets)

# Function to process and send captured packets
def render_row(packet):
    if IP in packet and (TCP in packet or UDP in packet):
        # Extract packet information
        source_address = packet[IP].src
        destination_address = packet[IP].dst

        if TCP in packet:
            protocol = 'TCP'
            source_port = packet[TCP].sport
            destination_port = packet[TCP].dport
        else:
            protocol = 'UDP'
            source_port = packet[UDP].sport
            destination_port = packet[UDP].dport

        packet_time = packet.time
        packet_length = len(packet)

        data_to_send = "{},{},{},{},{},{},{}".format(
            packet_time, protocol, source_address, source_port, destination_address, destination_port, packet_length
        )

        try:
            # Send the data to the server over HTTPS
            response = requests.post(server_url, data=data_to_send, verify=False)

            # Check the response status code to ensure the data was sent successfully
            if response.status_code == 200:
                print("Data sent successfully.")
            else:
                print("Error: {} - {}".format(response.status_code, response.text))
        except Exception as e:
            print("Error: {}".format(str(e)))

# Function to process captured packets
def render_content_from_pcap(captured_packets):
    frame_num = 0
    ignored_packets = 0

    for packet in captured_packets:
        frame_num += 1
        try:
            render_row(packet)
        except AttributeError:
            ignored_packets += 1

# Main function
def main():
    networkInterface = "eth0"  # Network interface to capture packets from
    capture_and_save(networkInterface)

if __name__ == "__main__":
    main()

