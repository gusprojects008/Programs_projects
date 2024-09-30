import struct
import socket

def bytes_to_mac(mac_bytes):
    return ':'.join(format(byte, '02x') for byte in mac_bytes)

def show_packet_hex(packet):
    return ' '.join(format(byte, '02x') for byte in packet)

def valid_ssid(ssid):
    if len(ssid) == 0 or len(ssid) > 32:
       return False
    for char in ssid:
        # IF CONDITION (32 <= ord(char) <= 126) IS FALSE IS RETURN false
        if not (32 <= ord(char) <= 126):           
           return False
    return True

# FOR EACH ESPECIFY FRAME IS NEEDED HANDLE THE PACKET IN DIFFERENT WAY 
# STRUCTURE PACKET MANAGEMENT:
# RADIOTAP HEADER 7 BYTES
# DATA FIELDS 9 BYTES
# 2 BYTES OR 4 HEXADECIMALS CHARS FOR FRAME CONTROL
# DURATION 2 BYTES
# 24 BYTES FOR ADDRESS
# SEQUENCE CONTROL 2 BYTES
# TIMESTAMP 8 BYTES
# BEACON INTERVAL 2 BYTES
# CAPABILITY INFORMATION 2 BYTES
# SSID RANDOM
# SUPPORTED RATES RANDOM

def dissec_packet(packet):
    packet_hex = packet.hex()
    length_packet = len(packet_hex)
    radiotap_length = int(packet_hex[4:6], 16)
#    data_field = packet_hex[]
    frame_control = packet_hex[radiotap_length*2:150]

    try:
       length_ssid = int(packet_hex[radiotap_length+21*2:], 16)
    except ValueError:
           length_ssid = None
    if length_ssid is not None:
       ssid = packet_hex[200:200+4+length_ssid*2]
    else:
        ssid = None
    
    if len(packet) > 250 and len(packet) < 500 and radiotap_length == 56:
       return f"Length PacketHex: {len(packet_hex)}, Radiotap Length: {radiotap_length}, Frame Control: {frame_control}, Length ssid: {length_ssid}, SSID: {ssid}, Hex Data: {packet_hex}, Packet UTF-8: {bytes.fromhex(packet_hex).decode('utf-8', errors='ignore')}\n"
     
#    if frame_control == '8000':
#       packet_beacon = {
#        "Length packet": length_packet,
#        "Radiotap length": radiotap_length,
#        "Frame Control": f"Management Beacon 0x{frame_control}",
#        "Length ssid": length_ssid,
#        "SSID": ssid
 #      }
 #      print(packet_beacon)
  #  elif frame_control == '5000':
  #       packet_probe = {
  #        "Length packet": length_packet,
  #        "Radiotap length": radiotap_length,
  #        "Frame Control": f"Management Probe response 0x{frame_control}",
  #        "Length ssid": length_ssid,
  #        "SSID": ssid
   #      }
    #     print(packet_probe)
   # elif frame_control == '8802':
 #        eapol_frame = f"Qos Data Eapol 0x{frame_control}"
  #       print(eapol_frame)
   
def intercept_packet():
    try:
       with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003)) as sock:
            sock.bind(('wlan0mon', 0))
            while True:
                  packet, address = sock.recvfrom(4096)
                  packet_found = dissec_packet(packet)
                  if packet_found:
                     print(packet_found)
    except Exception as error:
           print(f"Socket error ); {error}")
           sock.close()

intercept_packet()