from scapy.all import *
import os
import time


def packet_handler(packet, captured_packets):
    captured_packets.append(packet)


def capture_and_save_csv(networkInterface, output_csv_file):
    while True:
        current_timestamp = int(time.time())  # Generate a timestamp for the filenames
 #       print(f"Listening on {networkInterface}...")

        captured_packets = []

        # Capture network traffic for 5 seconds
        sniff(iface=networkInterface, prn=lambda packet: packet_handler(packet, captured_packets), timeout=5)

        # Save CSV file with a timestamp in the filename
        csv_file = '{}_{}.csv'.format(output_csv_file, current_timestamp)
        render_csv_from_pcap(captured_packets, csv_file)
        print("Data saved to {}".format(csv_file))


def render_csv_row(packet, fh_csv):
    if IP in packet and (TCP in packet or UDP in packet):
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

        csv_data = [packet_time, protocol, source_address, source_port, destination_address, destination_port,
                    packet_length]
        fh_csv.write(','.join(str(value) for value in csv_data) + '\n')


def render_csv_from_pcap(captured_packets, output_csv_file):
    frame_num = 0
    ignored_packets = 0

    with open(output_csv_file, 'w') as fh_csv:
        csv_header = "Time,Protocol,SourceIP,SourcePort,DestIP,DestPort,Length"
        fh_csv.write(csv_header + "\n")
        for packet in captured_packets:
            frame_num += 1
            try:
                render_csv_row(packet, fh_csv)
            except AttributeError:
                ignored_packets += 1

#    print('{} packets read, {} packets not written to CSV'.format(frame_num, ignored_packets))


def main():
    networkInterface = "eth0"
    output_csv_file = '/tmp/monitors/NET/net'

    capture_and_save_csv(networkInterface, output_csv_file)


if __name__ == "__main__":
    main()
