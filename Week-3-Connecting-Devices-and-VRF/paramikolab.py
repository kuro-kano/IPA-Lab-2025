""" paramikolab.py """
import paramiko
import os

def main():
    """Main function to execute the script."""
    connect_to_devices()

def get_private_key_path():
    """Get the path to the private key file."""
    return os.path.expanduser("~/.ssh/id_rsa")

def connect_to_devices():
    """Connect to network devices using Paramiko and retrieve configurations."""
    privatekey = get_private_key_path()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    network = ["172.31.16.1", "172.31.16.2", "172.31.16.3", "172.31.16.4", "172.31.16.5"]

    for index, ip in enumerate(network):
        try:
            print(f"Attempting to connect to {ip}...")

            ssh.connect(
                hostname=ip,
                username="admin",
                key_filename=privatekey,
                allow_agent=False,
                look_for_keys=False,
                disabled_algorithms=dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]),
            )
            print(f"Connected to {ip} successfully.")

            if index == 0:
                stdin, stdout, stderr = ssh.exec_command("show running-config")

                with open("R0_running_config.txt", "w") as file:
                    file.write(stdout.read().decode())

        except Exception as e:
            print(f"Failed to connect to {ip}: {e}")

        finally:
            if ssh.get_transport():
                ssh.close()

main()
