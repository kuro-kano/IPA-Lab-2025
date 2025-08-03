"""netmiko.py"""
from netmiko import ConnectHandler

USERNAME = 'admin'
PASSWORD = 'cisco'

def main():
  """Main function to configure devices using Netmiko."""
  configure_devices()

def configure_devices():
  """Function to configure devices using Netmiko."""
  configure_r1()
  configure_r2()
  configure_s1()

def configure_r1():
  """Function to configure R1 (CiscoIOSv-2, 172.31.16.4) using Netmiko."""
  pass

def configure_r2():
  """Function to configure R2 (CiscoIOSv-2, 172.31.16.5) using Netmiko."""
  pass

def configure_s1():
  """
  Function to configure S1 (CiscoIOSv-2, 172.31.16.2) using Netmiko.
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
    'ip address 10.0.101.1 255.255.255.0',
    'interface range g0/1-2',
    'switchport mode access',
    'switchport access vlan 101',
    'no shutdown',
  ]
  
  with ConnectHandler(**device_params) as ssh:
    print("Connected S1\nConfiguring S1...")
    result = ssh.send_config_set(commands)
    print(result)
    print("S1 configuration completed.")

main()