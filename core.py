import socket


class Server:

    def __init__(self, **kwargs):
        """Initialize a server object.

        Args:
            kwargs (optional): Optional overrides that will replace default settings. Defaults to None.
        """

        self.url = kwargs.get("url", "cabbages.servegame.com")
        self.udp_ports = kwargs.get("udp_ports", [7777, 7778])
        self.tcp_ports = kwargs.get("tcp_ports", 80)
        self.flag = kwargs.get("flag", ":flag_eu:")
        self.code = kwargs.get("code", "EU2")


class StatusManager:

    @staticmethod
    def server_worker(instance: Server, key: str):
        return StatusManager(instance, key, "").parse_current_status()

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

    def check_port_status(self, port: int):
        
        if port not in self.server.udp_ports:
            raise self.InvalidPortError

        return (
            f"{self.header}"
            f"\n\n{self.name}:{port}: Instance is {'running' if self.socket_connect(port) else 'available'}"
        )
    
    def socket_connect(self, ports: int, type='TCP'):
        """Checks if a UDP/TCP port is open on the server.

        Args:
            ports (int): The ports number to check.
            type (str): Port check type, Defaults to UDP

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

            print(True)
            return True
        
        except socket.timeout:
            print('timeout')
            return False
        
        except socket.error:
            print('error')
            return False
        
        finally:
            sock.close()

    def check_server_status(self):
        """Check the server status and store results
        """

        self.web = 'running :bulb:' if self.socket_connect(self.server.tcp_ports) else 'unavailable :wrench:'
        self.ports = ['up :white_check_mark:' if self.socket_connect(port, type='UDP') else 'down :x:' for port in self.server.udp_ports]

        for status in self.ports:
            if status == 'down :x:' and self.web == 'running :bulb:':
                self.downs += 1

    def parse_current_status(self):
        """Return a parsed a server status string containing all necessary information
        """
        return (
            f"{self.header}"
            f"\n\n**{self.server.code}** [{self.name.capitalize()}'s Server](http://{self.server.url}) {self.server.flag} | The Web UI is {self.web} and **{self.downs}/{len(self.server.udp_ports)}** instances are available"
            )

    class InvalidPortError(Exception):
        pass
