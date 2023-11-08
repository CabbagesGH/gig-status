import random
import socket


def check_udp_port(domain, udp_port):
    """Checks if a UDP port is open at a specific domain.

    Args:
        domain: The domain name or IP address to check.
        port: The port number to check.

    Returns:
        True if the port is open, False otherwise.
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    try:
        sock.sendto(b"", (domain, udp_port))
        data, addr = sock.recvfrom(1024)
        return True
    except socket.timeout:
        return False
    finally:
        sock.close()


def check_tcp_port(domain, tcp_port):
    """Checks if a TCP port is open at a specific domain.

    Args:
        domain: The domain name or IP address to check.
        port: The port number to check.

    Returns:
        True if the port is open, False otherwise.
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((domain, tcp_port))
        return True
    except socket.error:
        return False
    finally:
        sock.close()


cabbages_url = 'cabbages.servegame.com'
skillz_url = 'gig.illskillz.pro'
anhur_url = 'anhur.servegame.com'
syco_url = 'syco.servegame.com'
tcp_port80 = 80
tcp_port8081 = 8081
udp_port7777 = 7777
udp_port7778 = 7778
udp_port7779 = 7779
udp_port7780 = 7780


def check_server_status(server_url, tcp_port, udp_ports):
    web_status = 'running :bulb:' if check_tcp_port(server_url, tcp_port) else 'unavailable :wrench:'

    port_status = []
    for port in udp_ports:
        port_status.append('up :white_check_mark:' if check_udp_port(server_url, port) else 'down :x:')

    down_count = 0
    for status in port_status:
        if status == 'down :x:' and web_status == 'running :bulb:':
            down_count += 1
        else:
            down_count = 0

    return web_status, port_status, down_count


cabbages_web, cabbages_ports, cabbages_count = check_server_status(
    cabbages_url, tcp_port80, [udp_port7777, udp_port7778]
)

skillz_web, skillz_ports, skillz_count = check_server_status(
    skillz_url, tcp_port80, [udp_port7777, udp_port7778]
)

anhur_web, anhur_ports, anhur_count = check_server_status(
    anhur_url, tcp_port80, [udp_port7777, udp_port7778]
)

syco_web, syco_ports, syco_count = check_server_status(
    syco_url, tcp_port8081, [udp_port7777, udp_port7778, udp_port7779, udp_port7780]
)


def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == '!status':
        return (('>>> ## Gigantic Server Status'
                 '\n\n**EU3** [Cabbages\'s Server](http://{}) :flag_eu: | The Web UI is {} and **{}/2** instances are available'
                 '\n\n**EU2** [Skillz\'s Server](http://{}) :flag_eu: | The Web UI is {} and **{}/2** instances are available'
                 '\n\n**NA3** [Anhur\'s Server](http://{}) :flag_us: | The Web UI is {} and **{}/2** instances are available'
                 '\n\n**NA5** [Syco\'s Server](http://{}) :flag_us: | The Web UI is {} and **{}/4** instances are available')
                .format(cabbages_url, cabbages_web, cabbages_count,
                        skillz_url, skillz_web, skillz_count,
                        anhur_url, anhur_web, anhur_count,
                        syco_url, syco_web, syco_count,))

    if p_message == 'hello':
        return 'Hey there!'

    if message == 'roll':
        return str(random.randint(1, 6))

    if p_message == '!status help':
        return '`This is a help message that you can modify.`'

    return 'I didn\'t understand what you wrote. Try typing `!status help`.'
