"""testfsmlab.py"""
from netmiko import ConnectHandler
import os

USERNAME = 'admin'
SSH_KEY_FILE = os.path.expanduser("~/.ssh/id_rsa")

def configure_template(cdp_neighbor, config: list=[]):
  """Function to crete output template using Textfsm."""
  for neighbor in cdp_neighbor:
    local = neighbor['local_interface'].replace(" ", "")
    remote = neighbor['platform'] + " " + neighbor['neighbor_interface']
    name = neighbor['neighbor_name'].replace(".ipa.com", "")
    
    config.append(f'int {local}')
    config.append(f'description Connect to {remote} of {name}')
    config.append('exit')

  return config

def configure_r1():
  """
  Function to Show CDP on R1 (CiscoIOSv-2, 172.31.16.4) using Netmiko.
  """
  device_params = {
    'device_type': 'cisco_ios',
    'ip': '172.31.16.4',
    'username': USERNAME,
    'key_file': SSH_KEY_FILE,
    'use_keys': True,
    'allow_agent': False,
    'disabled_algorithms': dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]),
  }

  with ConnectHandler(**device_params) as ssh:
      print("Connected to R1")
      print("Running 'show cdp neighbors' command...")
      output = ssh.send_command("show cdp neighbors", use_textfsm=True)
      config = configure_template(output)
      config.extend(["int Gig0/1", "description Connect to PC", "exit"])
      
      result = ssh.send_config_set(config)
      print(result)
      print("R1 configuration completed.\n----------\n")

      ssh.disconnect()

def configure_r2():
  """
  Function to Show CDP on R2 (CiscoIOSv-2, 172.31.16.5) using Netmiko.
  """
  device_params = {
    'device_type': 'cisco_ios',
    'ip': '172.31.16.5',
    'username': USERNAME,
    'key_file': SSH_KEY_FILE,
    'use_keys': True,
    'allow_agent': False,
    'disabled_algorithms': dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]),
  }

  with ConnectHandler(**device_params) as ssh:
      print("Connected to R2")
      print("Running 'show cdp neighbors' command...")
      output = ssh.send_command("show cdp neighbors", use_textfsm=True)
      config = configure_template(output)
      config.extend(["int Gig0/1", "description Connect to WAN", "exit"])

      result = ssh.send_config_set(config)
      print(result)
      print("R2 configuration completed.\n----------\n")

      ssh.disconnect()

def configure_s1():
  """
  Function to Show CDP on R3 (CiscoIOSvL2-2, 172.31.16.3) using Netmiko.
  """
  device_params = {
    'device_type': 'cisco_ios',
    'ip': '172.31.16.3',
    'username': USERNAME,
    'key_file': SSH_KEY_FILE,
    'use_keys': True,
    'allow_agent': False,
    'disabled_algorithms': dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]),
  }
  
  with ConnectHandler(**device_params) as ssh:
      print("Connected to S1")
      print("Running 'show cdp neighbors' command...")
      output = ssh.send_command("show cdp neighbors", use_textfsm=True)
      config = configure_template(output)
      config.extend(["int Gig0/1", "description Connect to PC", "exit"])

      result = ssh.send_config_set(config)
      print(result)
      print("S1 configuration completed.\n----------\n")

      ssh.disconnect()