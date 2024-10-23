import socket
import struct
import psutil
import subprocess

class colors:
      red = "\033[31m"
      green = "\033[32m"
      blue = "\033[34m"
      cyan = "\033[36m"
      purple = "\033[35m"
      reset = "\033[0m"
      pink = "\033[95m"

      # FORMAT TEXT
      bright = '\033[1m'
      background_green = '\033[32m'
      background_red = '\033[41m'
      blink = '\033[5m'
      sublime = '\033[4m'

      # COLOR + BRIGHT
      sb = f'{bright}{sublime}'
      gb = f'{bright}{green}'
      bb = f'{bright}{blue}'

def show_interfaces_addrs():
    try:
       print()
       address_interfaces = psutil.net_if_addrs()
       for interfaces in address_interfaces:
           for info in address_interfaces.get(interfaces):
               if psutil.AF_LINK in info:
                  print(f"{colors.green}{info.address} => {colors.gb}{interfaces}{colors.reset}")
       print()
    except Exception as error:
           print(f"Error to get interfaces and address );\n{colors.red}{str(error)}{colors.reset}\n")

def set_interface_mode(iface_options):
    if iface_options == 0:
       print()
       interface_to_monitor = input(f"{colors.bright}Type it interface for set monitor mode: {colors.bright}{colors.blue}OBSERVATION: *Make Sure your managed interface is on the same channel as the monitor interface{colors.reset}: ")
       try:
          subprocess.run(['ip', 'link', 'set', interface_to_monitor, 'down'])
          subprocess.run(['iw', 'dev', interface_to_monitor, 'set', 'type', 'monitor'])
          subprocess.run(['ip', 'link', 'set', interface_to_monitor, 'up'])
       except Exception as error:
              print(f"Error to the set {interface_to_monitor} for monitor mode ); {str(error)}")

    elif iface_options == 1:
         print()
         add_interface_monitor = input(f"{colors.bright}Type it the interface wireless, for create a other interface virtual in monitor mode: {colors.reset}")
         try:
            subprocess.run(['iw', 'dev', add_interface_monitor, 'interface', 'add', 'wlan0monitor', 'type', 'monitor'])
            subprocess.run(['ip', 'link', 'set', 'wlan0monitor', 'up'])
         except Exception as error:
                print(f"Error to the create virtual interface in monitor mode ); {colors.red}{str(error)}{colors.reset}")
    else:
        print(f"Type it {colors.red}0{colors.reset} or {colors.green}1{colors.reset}")
    print()
    show_interfaces_addrs()

def return_mac(interface_network):
    addresses_interface = psutil.net_if_addrs()
    if interface_network in addresses_interface:
       for info in addresses_interface.get(interface_network):
           for address in info:
               if psutil.AF_LINK in info:
                  return info.address
    return None

def mac_for_bytes(mac):
    return bytes(int(byte, 16) for byte in mac.split(':'))

# fill with 0 if the byte have less than 2 digits, and transform into hexadecimal 02x 
def bytes_for_mac(mac):
    return ':'.join(format(byte, '02x') for byte in mac)

def compress_data(packet):
    return ''.join(format(byte, '02x') for byte in packet)

def idenfify_interface_mode(interface):
    try:
       infomations_iface = subrpocess.run(['iwconfig', interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=False)
       if "Mode:monitor" in informations_iface.stdout.decode('utf-8'):
          return True
       else:
           return False
    except Exception as error:
           print(f"Error ): it was not possible identify interface mode... {colors.red}{str(error)}, stderr: {information_iface.stderr}{colors.reset}")

def calc_rates(rates):
    list_rates_transmition = []
    for rate in rates:
        # OPERATION: AND BIT BY BIT, (rate binary & value hexadecimal: 0x7f/01111111) * 500 
        value_rate = (rate & 0x7f) * 500
        list_rates_transmition.append(f"{value_rate} Mbps")
    return list_rates_transmition

class Info_Packets:
      def __init__(self, interface):
          mac_interface = mac_for_bytes(return_mac(interface))
          self.RadioTapHeader = struct.pack('!BBH', 0x00, 0x00, 0x0056)
          #self.RadioInformation = struct.pack('!BB', 0x02, 0xd6)
          self.FrameControl = struct.pack('!H', 0x0040)
          self.MacHeader = struct.pack('!6s6s', b'\xff\xff\xff\xff\xff\xff', b'\xff\xff\xff\xff\xff\xff')
          self.FrameControl_Extension = struct.pack('!H', 4000)
          self.WirelessManagement = struct.pack('!BB', 0x00, 0x00)
          self.rates = struct.pack('!BB', 0x01, 0x08) + b'\x02\x04\x0b\x16\x0c\x12\x18\x24'

      def build_packet(self):
          packet = (self.FrameControl + self.MacHeader)
          return packet  

def SendPackets(interface_network):
    packets_info = Info_Packets(interface_network)
    packet_sent = packets_info.build_packet()
    try:
       with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003)) as sock:
            sock.bind((interface_network, 0))
            sock.send(packet_sent)
            print(f"\n{packet_sent.hex()}")
    except Exception as error:
           print(f"A Error occur ); {colors.red}\n{error}{colors.reset}\n")
           sock.close()

if __name__ == "__main__":
   show_interfaces_addrs()
   config_interfaces = int(input(f"{colors.bright}You want set interface? for monitor mode {colors.gb}(1 or 0){colors.reset}: {colors.reset}"))
   try:
      if config_interfaces == 1:
         show_interfaces_addrs()
         print(f"{colors.green}Type it: {colors.gb}0{colors.reset} {colors.green}to set a interface for monitor mode. {colors.purple}Type it: {colors.gb}1{colors.reset} {colors.purple}for add interface virtual in monitor mode:{colors.reset}\n")
         interface_monitor_option = int(input(f"{colors.green}You want: Set interface for monitor mode or add virtual interface in monitor mode? {colors.gb}1{colors.reset}/{colors.gb}0{colors.reset}: "))
         set_interface_mode(interface_monitor_option)
   except Exception as error:
          print(f"\nError to the set config ): or just option 0 (: {colors.red}{str(error)}{colors.reset}\n")
   print()
   interface = input(f"{colors.bright}Type it MANAGED interface Network for operation: {colors.reset}")
   SendPackets(interface)
