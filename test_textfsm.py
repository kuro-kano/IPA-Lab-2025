from textfsmlab import configure_r1, configure_r2, configure_s1
from netmiko import ConnectHandler
import os

USERNAME = 'admin'
SSH_KEY_FILE = os.path.expanduser("~/.ssh/id_rsa")

def main():
  """Main function to do TDD testing with Pytest."""
  testing_r1()
  testing_r2()
  testing_s1()

def testing_r1():
  """Function to do TDD of testing_r1"""
  configure_r1()

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
    desc = ssh.send_command("show int description", use_textfsm=True)

    interface = {d['port']: d['description'] for d in desc}
    assert interface["Gi0/0"] == "Connect to Gig 0/1 of S0"
    assert interface["Gi0/1"] == "Connect to PC"
    assert interface["Gi0/2"] == "Connect to Gig 0/1 of R2"

    ssh.disconnect()

def testing_r2():
  """"""
  configure_r2()

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
    desc = ssh.send_command("show int description", use_textfsm=True)

    interface = {d['port']: d['description'] for d in desc}
    assert interface["Gi0/0"] == "Connect to Gig 0/2 of S0"
    assert interface["Gi0/1"] == "Connect to WAN"
    assert interface["Gi0/2"] == "Connect to Gig 0/1 of S1"
    assert interface["Gi0/3"] == "Connect to Gig 0/1 of R0"

    ssh.disconnect()

def testing_s1():
  """"""
  configure_s1()
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
    desc = ssh.send_command("show int description", use_textfsm=True)

    interface = {d['port']: d['description'] for d in desc}
    assert interface["Gi0/0"] == "Connect to Gig 0/3 of S0"
    assert interface["Gi0/1"] == "Connect to PC"
    assert interface["Gi0/2"] == "Connect to Gig 0/1 of S1"
    assert interface["Gi0/3"] == "Connect to Gig 0/1 of R0"

    ssh.disconnect()

main()
