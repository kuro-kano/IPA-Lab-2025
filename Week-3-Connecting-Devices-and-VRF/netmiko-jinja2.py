"""netmiko-jinja2.py"""
from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader
import yaml

USERNAME = 'admin'
PASSWORD = 'cisco'

def main():
  """Main function to configure devices using Netmiko with Jinja2."""
  # Load the device information from a YAML 
  file_path = 'templates/device_info.yaml'

  with open(file_path, 'r') as file:
    info = yaml.safe_load(file)

  for device in info:
    configure_device(device)


def configure_device(device_info):
  """Function to configure a device using Netmiko with Jinja2 template."""

  env = Environment(loader=FileSystemLoader('templates'))
  template = env.get_template('devices_template.txt')
  
  device_params = {
    'device_type': device_info['device_type'],
    'ip': device_info['ip_address'],
    'username': USERNAME,
    'password': PASSWORD,
  }

  with ConnectHandler(**device_params) as ssh:
    print(f"Connected to {device_info['name']}:{device_info['ip_address']}\nConfiguring...")
    commands = template.render(device_info).strip()

    result = ssh.send_config_set(commands.splitlines())
    print(result)
    print(f"\n{device_info['ip']} configuration completed.\n----------\n")
