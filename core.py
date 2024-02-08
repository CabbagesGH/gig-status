import socket


# Server class for all server parameters to be held
class Server:

    def __init__(self, **kwargs):
        """Initialize a server object.

        Args:
            kwargs (optional): Optional overrides that will replace default kwargs. Defaults to the below.
        """

        self.url = kwargs.get("url", "cabbages.servegame.com")
        self.udp_ports = kwargs.get("udp_ports", [7777, 7778])
        self.tcp_ports = kwargs.get("tcp_ports", 80)
        self.flag = kwargs.get("flag", ":flag_eu:")
        self.code = kwargs.get("code", "EU2")


# All defined functions for checking server ports
class StatusManager:

    # Static method for threadpool implementation in responses
    @staticmethod
    def server_worker(instance: Server, key: str):
        return StatusManager(instance, key, "").parse_current_status()

    # Initialise server status manager
    def __init__(self, server: Server, name: str, header: str = ">>> ## Gigantic Server Status") -> None:
        """Initialize a server status manager.

        Args:
            server (Server): Server that needs management
            name (str): Server name
            header (str or None, optional): Parsed values header. Defaults to the base header 
            (should be empty when not needed).
        """

        self.name = name
        self.server = server
        self.header = header if header else ""

        self.web = None
        self.ports = None
        self.downs = 0

        # Check for server status at init time since it's almost always needed
        self.check_server_status()

    # Single port checker
    def check_port_status(self, port: int):

        # If port not used for specified server
        if port not in self.server.udp_ports:
            raise self.InvalidPortError

        return (
            f"{self.header}"
            f"\n\n{self.name.capitalize()} {port}: Instance is {'running' if self.socket_connect(port, type='UDP') else 'available'}"
        )

    # TCP/UDP port checking handler
    def socket_connect(self, ports: int, type='TCP'):
        """Checks if a UDP/TCP port is open on the server.

        Args:
            ports (int): The ports number to check.
            type (str): Port check type, Defaults to TCP

        Returns:
            True if the port is open, False otherwise.
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM if type == "UDP" else socket.SOCK_STREAM)
        sock.settimeout(0.4)

        try:

            if type == "UDP":
                sock.sendto(b"", (self.server.url, ports))

                # Is this needed ?
                data, addr = sock.recvfrom(1024)

            else:
                sock.connect((self.server.url, ports))

            return True
        
        except socket.timeout:
            return False
        
        except socket.error:
            return False
        
        finally:
            sock.close()

    # Server web status checker and available port counter
    def check_server_status(self):
        """Check the server status and store results
        """

        self.web = 'running :bulb:' if self.socket_connect(self.server.tcp_ports) else 'unavailable :wrench:'
        self.ports = ['up :white_check_mark:' if self.socket_connect(port, type='UDP') else 'down :x:' for port in self.server.udp_ports]

        for status in self.ports:
            if status == 'down :x:' and self.web == 'running :bulb:':
                self.downs += 1

    # Sets up header and status message for full status check and single server status check
    def parse_current_status(self):
        """Return a parsed server status string containing all necessary information
        """
        return (
            f"{self.header}"
            f"\n\n**{self.server.code}** [{self.name.capitalize()}'s Server](http://{self.server.url}) {self.server.flag} | The Web UI is {self.web} and **{self.downs}/{len(self.server.udp_ports)}** instances are available"
            )

    # Invalid port exception, passes to exception handler in responses.py
    class InvalidPortError(Exception):
        pass
