from scapy.all import rdpcap, IP, TCP, UDP

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

        csv_data = [packet_time, protocol, source_address, source_port, destination_address, destination_port, packet_length]
        fh_csv.write(','.join(str(value) for value in csv_data) + '\n')

def main():
    input_pcap_file = 'captured_traffic.pcap'
    output_csv_file = 'captured_traffic_processed.csv'

    packets = rdpcap(input_pcap_file)

    frame_num = 0
    ignored_packets = 0

    with open(output_csv_file, 'w') as fh_csv:
        csv_header = "Time,Protocol,SourceIP,SourcePort,DestIP,DestPort,Length"
        fh_csv.write(csv_header + "\n")
        for packet in packets:
            frame_num += 1
            try:
                render_csv_row(packet, fh_csv)
            except AttributeError:
                ignored_packets += 1

    print('{} packets read, {} packets not written to CSV'.format(frame_num, ignored_packets))

if __name__ == "__main__":
    main()

