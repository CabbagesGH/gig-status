import socket
import re


def check_udp_port(domain, udp_port):
    """Checks if a UDP port is open at a specific domain.

    Args:
        domain: The domain name or IP address to check.
        udp_port: The port number to check.

    Returns:
        True if the port is open, False otherwise.
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.4)
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
        tcp_port: The port number to check.

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


# Gigantic Servers JSON, all data needed to check status
servers = {
    'cabbages': {
        'url': 'cabbages.servegame.com',
        'udp_ports': [7777, 7778],
        'tcp_port': 80,
        'flag': ':flag_eu:',
        'code': 'EU3'
    },
    'skillz': {
        'url': 'gig.illskillz.pro',
        'udp_ports': [7777],
        'tcp_port': 80,
        'flag': ':flag_eu:',
        'code': 'EU2'
    },
    'anhur': {
        'url': 'anhur.servegame.com',
        'udp_ports': [7777, 7778],
        'tcp_port': 80,
        'flag': ':flag_us:',
        'code': 'NA3'
    },
    'syco': {
        'url': 'syco.servegame.com',
        'udp_ports': [7777, 7778, 7779, 7780],
        'tcp_port': 8081,
        'flag': ':flag_us:',
        'code': 'NA5'
    }
}

# Simplifies some later code
cabbages_url = servers.get('cabbages')['url']
skillz_url = servers.get('skillz')['url']
anhur_url = servers.get('anhur')['url']
syco_url = servers.get('syco')['url']


# Checks the status of all Gigantic servers and available instances
def check_server_status(server_url, tcp_port, udp_ports):
    web_status = 'running :bulb:' if check_tcp_port(server_url, tcp_port) else 'unavailable :wrench:'

    port_status = []
    for port in udp_ports:
        port_status.append('up :white_check_mark:' if check_udp_port(server_url, port) else 'down :x:')

    down_count = 0
    for status in port_status:
        if status == 'down :x:' and web_status == 'running :bulb:':
            down_count += 1

    return web_status, port_status, down_count


# Checks individual ports a user specifies
def check_port_status(server_name, port_number):
    server_data = servers.get(server_name)
    if server_data is None:
        return 'Invalid server name'

    server_url = server_data['url']
    udp_ports = server_data['udp_ports']

    if port_number not in udp_ports:
        return 'Invalid port number for this server'

    return (('>>> ### Gigantic Server Status'
             '\n\n{} {}: This instance is running')
            .format(server_name.capitalize(), port_number)) if check_udp_port(server_url,
                                                                              port_number) else (
        ('>>> ### Gigantic Server Status'
         '\n\n{} {}: This instance is available')
        .format(server_name.capitalize(), port_number))


# Checks individual server status
def check_server_name_status(server_url, tcp_port, udp_ports):
    web_status = 'running :bulb:' if check_tcp_port(server_url, tcp_port) else 'unavailable :wrench:'

    port_status = []
    for port in udp_ports:
        port_status.append('up :white_check_mark:' if check_udp_port(server_url, port) else 'down :x:')

    down_count = 0
    for status in port_status:
        if status == 'down :x:' and web_status == 'running :bulb:':
            down_count += 1

    return web_status, port_status, down_count


# Responses
def get_response(message: str) -> str:
    p_message = message.lower()

    # Extract server name from user's input
    match_server_check = re.search(r'!status\s+(\w+)', p_message)

    # Extract server name and port number from the user's input
    match_port_check = re.search(r'!status\s+(\w+)\s+(\d+)', p_message)

    # If just status is invoked show full server list and statuses
    if p_message == '!status':
        cabbages_web, cabbages_ports, cabbages_count = check_server_status(
            servers.get('cabbages')['url'], servers.get('cabbages')['tcp_port'], servers.get('cabbages')['udp_ports']
        )

        skillz_web, skillz_ports, skillz_count = check_server_status(
            servers.get('skillz')['url'], servers.get('skillz')['tcp_port'], servers.get('skillz')['udp_ports']
        )

        anhur_web, anhur_ports, anhur_count = check_server_status(
            servers.get('anhur')['url'], servers.get('anhur')['tcp_port'], servers.get('anhur')['udp_ports']
        )

        syco_web, syco_ports, syco_count = check_server_status(
            servers.get('syco')['url'], servers.get('syco')['tcp_port'], servers.get('syco')['udp_ports']
        )
        return ('>>> ## Gigantic Server Status'
                '\n\n**EU3** [Cabbages\'s Server](http://{}) :flag_eu: | The Web UI is {} and **{}/2** instances are available'
                '\n\n**EU2** [Skillz\'s Server](http://{}) :flag_eu: | The Web UI is {} and **{}/1** instances are available'
                '\n\n**NA3** [Anhur\'s Server](http://{}) :flag_us: | The Web UI is {} and **{}/2** instances are available'
                '\n\n**NA5** [Syco\'s Server](http://{}) :flag_us: | The Web UI is {} and **{}/4** instances are available'
                .format(cabbages_url, cabbages_web, cabbages_count,
                        skillz_url, skillz_web, skillz_count,
                        anhur_url, anhur_web, anhur_count,
                        syco_url, syco_web, syco_count))

    # Shows a guide for user
    if p_message == '!status help':
        return ('>>> ### Gigantic Server Status Guide'
                '\n\nCommands are:'
                '\n\n`!status`: full server list'
                '\n`!status <server_name>`: to see the status for a specific server, for example`!status anhur`'
                '\n`!status <server_name> <instance_number>`: to see the status of a specific instance of a server, for example`!status syco 7777`'
                '\nAdd `?` at the beginning to send it to you via DM, for example `?!status skillz`')

    # If port check matches then return single instance return message
    if match_port_check:
        server_name = match_port_check.group(1)
        port_number = int(match_port_check.group(2))

        return check_port_status(server_name, port_number)

    # If server check matches then return single server return message
    if match_server_check:
        server_name = match_server_check.group(1)
        web, ports, count = check_server_status(
            servers.get(server_name)['url'], servers.get(server_name)['tcp_port'], servers.get(server_name)['udp_ports']
        )

        return ('>>> ### Gigantic Server Status'
                '\n\n**{}** [{}\'s Server](http://{}) {} | The Web UI is {} and **{}/{}** instances are available'
                .format(servers.get(server_name)['code'],
                        server_name.capitalize(),
                        servers.get(server_name)['url'],
                        servers.get(server_name)['flag'],
                        web,
                        count,
                        servers.get(server_name)['udp_ports'].__len__()
                        )
                )

    # Else if status command is invoked by user but parameters are invalid
    elif '!status' in p_message:
        return 'Invalid command. Use `!status help` to see see the guide'
