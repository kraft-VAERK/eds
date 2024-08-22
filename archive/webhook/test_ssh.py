import socket
import time
import paramiko
import os
import json

def check_ssh_connection(ip_address, ssh_key_path, username='ucloud'):
    """
    Check whether it's possible to establish an SSH connection with the provided IP address and SSH key.

    Args:
        ip_address (str): The IP address of the remote host.
        ssh_key_path (str): The path to the SSH private key file.

    Returns:
        bool: True if the SSH connection was successful, False otherwise.
    """
    try:
        # Create a new SSH client
        ssh_client = paramiko.SSHClient()
        
        print(f"Connecting to {ip_address} with key {ssh_key_path}")

        # Set policy to automatically add the hostname and check SSH key
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Load the private key for authentication
        private_key = paramiko.Ed25519Key.from_path(ssh_key_path)

        # Connect to the remote host
        ssh_client.connect(hostname=ip_address, username=username, pkey=private_key)

        # If connection is successful, return True
        return True
    except Exception as e:
        # If any exception occurs, return False
        print(f"Error: {e}")
        return False
    finally:
        # Close the SSH connection
        ssh_client.close()
def start_ssh_tunnel(ssh_private_key_path=None, remote_host=None, remote_port=None, local_port=None):
    """
    Start an SSH tunnel from local_port to remote_host:remote_port via SSH connection.

    Args:
        ssh_host (str): SSH server hostname or IP address.
        ssh_port (int): SSH server port.
        ssh_username (str): SSH username.
        ssh_private_key_path (str): Path to SSH private key file.
        remote_host (str): Remote host to tunnel to.
        remote_port (int): Remote port to tunnel to.
        local_port (int): Local port to forward to.

    Returns:
        paramiko.Channel: SSH tunnel channel.
    """
    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Load the private key
    private_key = paramiko.Ed25519Key.from_path(ssh_private_key_path)

    # Connect to the SSH server
    ssh_client.connect(hostname=remote_host, port=22, username="ucloud", pkey=private_key)

    # Start the SSH tunnel
    # tunnel = ssh_client.get_transport().open_channel('direct-tcpip', (remote_host, remote_port), ('localhost', local_port))
    ssh_client.close()

    return "OK"
def is_tunnel_running(local_port):
    """
    Test if an SSH tunnel is already running by attempting to connect to the local port.

    Args:
        local_port (int): Local port to test.

    Returns:
        bool: True if the tunnel is running, False otherwise.
    """
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Attempt to connect to the local port
        sock.connect(('localhost', local_port))
        return True
    except ConnectionRefusedError:
        return False
    finally:
        # Close the socket
        sock.close()
while True:
    json_file_path = 'machines.json'
    # Open the JSON file in read mode
    with open(json_file_path, 'r') as json_file:
        # Load the JSON data from the file
        data = json.load(json_file)
    for x in data:
        if check_ssh_connection(x["ip"], x["ssh_key"]):
            print("SSH connection is possible.")
            if is_tunnel_running(int(x["port"])):
                print(f"SSH tunnel to {x['name']} is already running.")
            else: 
                os.system(f"ssh -Nf -L {x['port']}:localhost:8080 -i {x['ssh_key']} ucloud@{x['ip']}")
                print(f"SSH tunnel to {x['name']} started.")
        else:
            print("Unable to establish SSH connection.")
    time.sleep(3600)