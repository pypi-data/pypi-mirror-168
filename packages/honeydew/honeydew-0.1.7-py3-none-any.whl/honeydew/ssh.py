import paramiko
from paramiko import SSHClient
from scp import SCPClient
class SshConnector:
    """Instantiate an SSH connector.
    Args:
        host (str): SSH host
        port (str): SSH port
        private_key (str): SSH private key file path
        username (str): SSH user
        disable_rsa_512_256 (boolean): If the value is True, then rsa-sha2-512 and rsa-sha2-256 algorithm will be disabled
    """    
    def __init__(self, host, port, private_key, username, disable_rsa_512_256=False):
        self.host = host
        self.port = port
        self.private_key = private_key
        self.username = username
        self.disable_rsa_512_256 = disable_rsa_512_256
        
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.key = paramiko.RSAKey.from_private_key_file(self.private_key)
        if self.disable_rsa_512_256 == False:
            self.ssh.connect(self.host, port=self.port, username=self.username, pkey=self.key, timeout=3600)
        else:
            self.ssh.connect(self.host, port=self.port, username=self.username, pkey=self.key, timeout=3600, disabled_algorithms=dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]))
        
    def scp_upload(self, src, dst):
        """
        Upload a file with SCP
        Args:
            src (str): Path of source file
            dst (str): Path of destination file
        Returns:
            result (str): The result of function
        """        
        scp = SCPClient(self.ssh.get_transport())
        scp.put(src, dst)    
        return """{src} has been uploaded!""".format(src=src)

    def scp_download(self, src, dst):
        """
        Download a file with SCP
        Args:
            src (str): Path of source file
            dst (str): Path of destination file
        Returns:
            result (str): The result of function
        """                
        scp = SCPClient(self.ssh.get_transport())
        scp.get(src, dst)    
        return """{src} has been downloaded!""".format(src=src)