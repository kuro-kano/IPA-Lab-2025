"""netmiko.py"""
from netmiko import ConnectHandler

USERNAME = 'admin'
PASSWORD = 'cisco'

def main():
  """Main function to configure devices using Netmiko."""
  configure_r1()
  configure_r2()
  configure_s1()

def configure_devices(device_params, commands, device_name):
  """Function to configure devices using Netmiko."""
  with ConnectHandler(**device_params) as ssh:
    print(f"Connected {device_name}\nConfiguring {device_name}...")
    result = ssh.send_config_set(commands)
    print(result)
    print(f"\n{device_name} configuration completed.\n----------\n")

def configure_r1():
  """
  Function to configure R1 (CiscoIOSv-2, 172.31.16.4) using Netmiko.
  Configures OSPF and loopback interface.
  """
  ip_address = '172.31.16.4'
  
  device_params = {
    'device_type': 'cisco_ios',
    'ip': ip_address,
    'username': USERNAME,
    'password': PASSWORD,
  }

  commands = [
    # OSPF configuration
    'router ospf 1',
    'router-id 1.1.1.1',
    'network 10.0.0.0 0.0.0.255 area 0', # R1 -> Ubuntu
    'network 10.0.1.0 0.0.0.255 area 0', # R1 -> R2
    'network 10.255.1.1 0.0.0.0 area 0', # R1 -> Loopback

    # Loopback Configuration
    'int lo0',
    'ip add 10.255.1.1 255.255.255.255', # loopback interface
    'no shut',
    # 'ip ospf 1 area 0',
    ]

  configure_devices(device_params, commands, "R1")

def configure_r2():
  """
  Function to configure R2 (CiscoIOSv-2, 172.31.16.5) using Netmiko.
  Configures OSPF, loopback interface, and NAT.
  """
  ip_address = '172.31.16.5'

  device_params = {
    'device_type': 'cisco_ios',
    'ip': ip_address,
    'username': USERNAME,
    'password': PASSWORD,
  }

  commands = [
    # OSPF configuration
    'router ospf 1',
    'router-id 2.2.2.2',
    'network 10.0.101.0 0.0.0.255 area 0', # R2 -> S1
    'network 10.0.1.0 0.0.0.255 area 0', # R2 -> R1
    'network 10.255.2.2 0.0.0.0 area 0', # R2 -> Loopback
    'default-information originate',

    # Loopback Configuration
    'int lo0',
    'ip add 10.255.2.2 255.255.255.255',
    'no shut',
    # 'ip ospf 1 area 0',
    'exit',

    # NAT configuration
    'int range g0/1-2',
    'ip nat inside',
    'int g0/3',
    'ip nat outside',
    'exit',
    'access-list 1 permit 10.0.0.0 0.0.255.255',
    'ip nat inside source list 1 int g0/3 overload',
  ]

  configure_devices(device_params, commands, "R2")

def configure_s1():
  """
  Function to configure S1 (CiscoIOSv-2, 172.31.16.3) using Netmiko.
  Configures VLAN 101 on Interface g0/1-2.
  """
  ip_address = '172.31.16.3'

  device_params = {
    'device_type': 'cisco_ios',
    'ip': ip_address,
    'username': USERNAME,
    'password': PASSWORD,
  }

  commands = [
    'vlan 101',
    'name VLAN101',
    'exit',
    'interface vlan 101',
    'ip address 10.0.101.2 255.255.255.0',
    'interface range g0/1, g1/1',
    'switchport mode access',
    'switchport access vlan 101',
    'no shutdown',
  ]

  configure_devices(device_params, commands, "S1")

main()