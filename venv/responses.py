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


syco_url = "syco.servegame.com"
cabbages_url = "cabbages.servegame.com"
tcp_port80 = 80
tcp_port8081 = 8081
udp_port7777 = 7777
udp_port7778 = 7778
udp_port7779 = 7779
udp_port7780 = 7780

syco_web = 'running :bulb:' if check_tcp_port(syco_url, tcp_port8081) else 'unavailable :wrench:'
syco7777 = 'up :white_check_mark:' if check_udp_port(syco_url, udp_port7777) else 'down :x:'
syco7778 = 'up :white_check_mark:' if check_udp_port(syco_url, udp_port7778) else 'down :x:'
syco7779 = 'up :white_check_mark:' if check_udp_port(syco_url, udp_port7779) else 'down :x:'
syco7780 = 'up :white_check_mark:' if check_udp_port(syco_url, udp_port7780) else 'down :x:'

cabbages_web = 'running :bulb:' if check_tcp_port(cabbages_url, tcp_port80) else 'unavailable :wrench:'
cabbages7777 = 'up :white_check_mark:' if check_udp_port(cabbages_url, udp_port7777) else 'down :x:'
cabbages7778 = 'up :white_check_mark:' if check_udp_port(cabbages_url, udp_port7778) else 'down :x:'


def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == '!status':
        return (('>>> ## Gigantic Server Status'
                 '\n\n[Syco\'s Server](http://{}) :flag_us: | The Web UI is {} and instance {} is {}.'
                 '\n\n[Cabbages\'s Server](http://{}) :flag_eu: | The Web UI is {} and instance {} is {}.')
                .format(syco_url, syco_web, udp_port7777, syco7777,
                        cabbages_url, cabbages_web, udp_port7777, cabbages7777))

    if p_message == 'hello':
        return 'Hey there!'

    if message == 'roll':
        return str(random.randint(1, 6))

    if p_message == '!help':
        return '`This is a help message that you can modify.`'

    return 'I didn\'t understand what you wrote. Try typing `!help`.'
