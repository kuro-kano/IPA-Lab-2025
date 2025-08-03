"""netmiko-re.py"""
from netmiko import ConnectHandler
import re, os

USERNAME = 'admin'
SSH_KEY_FILE = os.path.expanduser("~/.ssh/id_rsa")

devices = [
    {
        'ip': '172.31.16.4',
        'device_type': 'cisco_ios',
        'username': USERNAME,
        'key_file': SSH_KEY_FILE,
        'use_keys': True,
        'allow_agent': False,
        'disabled_algorithms': dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]),
        'conn_timeout': 30,
    },
    {
        'ip': '172.31.16.5',
        'device_type': 'cisco_ios',
        'username': USERNAME,
        'key_file': SSH_KEY_FILE,
        'use_keys': True,
        'allow_agent': False,
        'disabled_algorithms': dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]),
        'conn_timeout': 30,
    }
]

def main():
  """Main function to configure devices using Netmiko with regex."""
  for device in devices:
    try:
      print(f"Connecting to {device['ip']}...")
      with ConnectHandler(**device) as ssh:
        print(f"Connected successfully.")

        int_output = ssh.send_command("show ip interface brief")
        active_interfaces = get_active_interfaces(int_output)

        v_output = ssh.send_command("show version")
        uptime = get_uptime(v_output)

        print(f"\n--- {device['ip']} ---")
        print(f"Uptime: {uptime}")
        print("Active Interfaces:")
        if active_interfaces:
            for interface, ip in active_interfaces:
                print(f" -  {interface}: {ip}")
        else:
            print("  No active interfaces found.")
        print("----------------------------------\n")

    except Exception as e:
        print(f"Failed to connect to {device['ip']}: {e}\n")

def get_active_interfaces(output):
  """Function to retrieve active interfaces using regex."""
  pattern = r'(?:(\S+\d+/\d+|\S+\d+)\s+(\d+\.\d+\.\d+\.\d+)).*up.*up'
  match = re.findall(pattern, output)

  if match:
    return match
  return None

def get_uptime(output):
  """Function to retrieve device uptime using regex."""
  pattern = r'uptime is (.*)'
  match = re.search(pattern, output)

  if match:
    return match.group(1).strip()
  return "Uptime not found"

main()
