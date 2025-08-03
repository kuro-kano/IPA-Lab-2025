"""netmiko-re.py"""
from netmiko import ConnectHandler
import re

USERNAME = 'admin'
PASSWORD = 'cisco'

devices = [
    {
        'name': 'R1',
        'ip': '172.31.16.4',
        'device_type': 'cisco_ios',
        'username': USERNAME,
        'password': PASSWORD,
    },
    {
        'name': 'R2',
        'ip': '172.31.16.5',
        'device_type': 'cisco_ios',
        'username': USERNAME,
        'password': PASSWORD,
    }
]

def main():
  """Main function to configure devices using Netmiko with regex."""
  pass

def get_active_interfaces(output):
  """Function to retrieve active interfaces using regex."""
  pattern = r'(\S+)\s+([0-9.]+)\s+YES\s+configured\s+up\s+up'
  match = re.search(pattern, output)

def get_uptime(output):
  """Function to retrieve device uptime using regex."""
  pattern = r'uptime is (.*)'
  match = re.search(pattern, output)

main()
