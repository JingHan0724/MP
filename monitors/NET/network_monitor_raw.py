from scapy.all import *
import os

def packet_handler(packet, captured_packets):
    captured_packets.append(packet)
 #   print("Packet Captured:")
 #   print(packet)

def capture_and_save_pcap(networkInterface, output_pcap_file, output_csv_file, capture_duration):
    # capture network traffic
    print("listening on %s" % networkInterface)
    captured_packets = []
    sniff(iface=networkInterface, prn=lambda packet: packet_handler(packet, captured_packets), timeout=capture_duration)
    # save pcap file
    wrpcap(output_pcap_file, captured_packets)
    print("Capture complete. Data saved to %s" % output_pcap_file)
    # save csv file
    os.system("tshark -N n -r {} -T fields -e frame.number -e _ws.col.Time -e _ws.col.Source -e _ws.col.Destination -e _ws.col.Protocol -e _ws.col.Length -e _ws.col.Info -E header=y -E separator=, > {}".format(output_pcap_file, output_csv_file))
    print("Data saved to %s" % output_csv_file)

def main():
    networkInterface = "eth0"
    output_pcap_file = 'captured_traffic.pcap'
    output_csv_file = 'captured_traffic.csv'
    capture_duration = 10  # Set the desired capture duration in seconds

    capture_and_save_pcap(networkInterface, output_pcap_file, output_csv_file, capture_duration)

if __name__ == "__main__":
    main()

