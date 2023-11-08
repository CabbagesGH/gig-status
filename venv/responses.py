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

cabbages_web = 'running :bulb:' if check_tcp_port(cabbages_url, tcp_port80) else 'unavailable :wrench:'
cabbages7777 = 'up :white_check_mark:' if check_udp_port(cabbages_url, udp_port7777) else 'down :x:'
cabbages7778 = 'up :white_check_mark:' if check_udp_port(cabbages_url, udp_port7778) else 'down :x:'
cabbages_ports = [cabbages7777, cabbages7778]
cabbages_count = 0

for port in cabbages_ports:
    if port == 'down :x:':
        cabbages_count += 1

skillz_web = 'running :bulb:' if check_tcp_port(skillz_url, tcp_port80) else 'unavailable :wrench:'
skillz7777 = 'up :white_check_mark:' if check_udp_port(skillz_url, udp_port7777) else 'down :x:'
skillz7778 = 'up :white_check_mark:' if check_udp_port(skillz_url, udp_port7778) else 'down :x:'
skillz_ports = [skillz7777, skillz7778]
skillz_count = 0

for port in skillz_ports:
    if port == 'down :x:':
        skillz_count += 1

anhur_web = 'running :bulb:' if check_tcp_port(anhur_url, tcp_port80) else 'unavailable :wrench:'
anhur7777 = 'up :white_check_mark:' if check_udp_port(anhur_url, udp_port7777) else 'down :x:'
anhur7778 = 'up :white_check_mark:' if check_udp_port(anhur_url, udp_port7778) else 'down :x:'
anhur_ports = [anhur7777, anhur7778]
anhur_count = 0

for port in anhur_ports:
    if port == 'down :x:':
        anhur_count += 1

syco_web = 'running :bulb:' if check_tcp_port(syco_url, tcp_port8081) else 'unavailable :wrench:'
syco7777 = 'up :white_check_mark:' if check_udp_port(syco_url, udp_port7777) else 'down :x:'
syco7778 = 'up :white_check_mark:' if check_udp_port(syco_url, udp_port7778) else 'down :x:'
syco7779 = 'up :white_check_mark:' if check_udp_port(syco_url, udp_port7779) else 'down :x:'
syco7780 = 'up :white_check_mark:' if check_udp_port(syco_url, udp_port7780) else 'down :x:'
syco_ports = [syco7777, syco7778, syco7779, syco7780]
syco_count = 0

for port in syco_ports:
    if port == 'down :x:':
        syco_count += 1


def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == '!status':
        return (('>>> ## Gigantic Server Status'
                 '\n\n**EU3** [Cabbages\'s Server](http://{}) :flag_eu: | The Web UI is {} and **{}/2** instances are available'
                 '\n\n**EU2**[Skillz\'s Server](http://{}) :flag_eu: | The Web UI is {} and **{}/2** instances are available'
                 '\n\n**NA3**[Anhur\'s Server](http://{}) :flag_us: | The Web UI is {} and **{}/2** instances are available'
                 '\n\n**NA5**[Syco\'s Server](http://{}) :flag_us: | The Web UI is {} and **{}/4** instances are available')
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
