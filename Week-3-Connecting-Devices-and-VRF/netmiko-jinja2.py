"""netmiko-jinja2.py"""
from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader
import yaml, os

USERNAME = 'admin'
PASSWORD = 'cisco'

def main():
  """Main function to configure devices using Netmiko with Jinja2."""
  # Load the device information .YAML
  script_dir = os.path.dirname(os.path.abspath(__file__))
  file_path = os.path.join(script_dir, 'templates', 'devices_info.yaml')

  try:
    with open(file_path, 'r') as file:
      info = yaml.safe_load(file)
  except FileNotFoundError:
    print(f"Error: The file {file_path} does not exist.")
    return
  
  template_dir = os.path.join(script_dir, 'templates')
  env = Environment(loader=FileSystemLoader(template_dir))
  template = env.get_template('devices_template.txt')

  for device in info:
    configure_device(device, template)

def configure_device(device, template):
  """Function to configure a device using Netmiko with Jinja2 template."""

  device_params = {
    'device_type': device['device_type'],
    'ip': device['ip_address'],
    'username': USERNAME,
    'password': PASSWORD,
  }

  with ConnectHandler(**device_params) as ssh:
    print(f"Connected to {device['name']}:{device['ip_address']}\nConfiguring...")
    commands = template.render(device).strip()

    result = ssh.send_config_set(commands.splitlines())
    print(result)
    print(f"\n{device['ip_address']} configuration completed.\n----------\n")

main()
