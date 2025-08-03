from netmiko import ConnectHandler
import time

# Device connection parameters
s1 = {
    'device_type': 'cisco_ios',
    'ip': 'S1_MANAGEMENT_IP',
    'username': 'admin',
    'password': 'cisco',
    'secret': 'cisco'  # Enable password
}

r1 = {
    'device_type': 'cisco_ios',
    'ip': 'R1_MANAGEMENT_IP',
    'username': 'admin',
    'password': 'cisco',
    'secret': 'cisco'
}

r2 = {
    'device_type': 'cisco_ios',
    'ip': 'R2_MANAGEMENT_IP',
    'username': 'admin',
    'password': 'cisco',
    'secret': 'cisco'
}

def configure_s1():
    print("Configuring S1...")
    net_connect = ConnectHandler(**s1)
    net_connect.enable()
    
    # Configure VLAN 101 for control/data plane
    commands = [
        'vlan 101',
        'name Control_Data_Plane',
        'exit',
        'interface range gi1/0-3',  # Adjust interface range as needed
        'switchport mode access',
        'switchport access vlan 101',
        'no shutdown',
        'exit'
    ]
    
    net_connect.send_config_set(commands)
    net_connect.disconnect()
    print("S1 configuration completed.")

def configure_r1():
    print("Configuring R1...")
    net_connect = ConnectHandler(**r1)
    net_connect.enable()
    
    # Configure OSPF on R1
    commands = [
        'router ospf 1',
        'network 0.0.0.0 255.255.255.255 area 0',
        'exit',
        'ip access-list standard MGMT_ACCESS',
        'permit Lab306_NETWORK',
        'permit MGMT_NETWORK',
        'exit',
        'line vty 0 4',
        'access-class MGMT_ACCESS in',
        'login local',
        'transport input ssh telnet',
        'exit'
    ]
    
    net_connect.send_config_set(commands)
    net_connect.disconnect()
    print("R1 configuration completed.")

def configure_r2():
    print("Configuring R2...")
    net_connect = ConnectHandler(**r2)
    net_connect.enable()
    
    # Configure OSPF and default route advertisement on R2
    commands = [
        'router ospf 1',
        'network 0.0.0.0 255.255.255.255 area 0',
        'default-information originate',
        'exit',
        # Configure PAT
        'ip access-list standard NAT_ACL',
        'permit any',
        'exit',
        'ip nat inside source list NAT_ACL interface GigabitEthernet0/1 overload',
        'interface GigabitEthernet0/0',  # Inside interface
        'ip nat inside',
        'exit',
        'interface GigabitEthernet0/1',  # Outside interface
        'ip nat outside',
        'exit',
        # Configure management access
        'ip access-list standard MGMT_ACCESS',
        'permit Lab306_NETWORK',
        'permit MGMT_NETWORK',
        'exit',
        'line vty 0 4',
        'access-class MGMT_ACCESS in',
        'login local',
        'transport input ssh telnet',
        'exit'
    ]
    
    net_connect.send_config_set(commands)
    net_connect.disconnect()
    print("R2 configuration completed.")

def main():
    try:
        configure_s1()
        configure_r1()
        configure_r2()
        print("All configurations completed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
