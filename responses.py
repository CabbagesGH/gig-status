import socket
import re
from core import Server, StatusManager

# Define base servers
servers = {
    "cabbages": Server(),
    "skillz": Server({"url": "gig.illskillz.pro", "udp_ports": [7777]}),
    "anhur": Server({"url": "anhur.servegame.com", "flag": ":flag_us:", "code": "NA3"}),
    "syco": Server({
        "url": "syco.servegame.com", 
        "udp_ports": [7777, 7778, 7779, 7780],
        "tcp_ports": 8081,
        "flag": ":flag_us:", 
        "code": "NA5"
    }),
}


# Responses
def get_response(message: str) -> str:
    p_message = message.lower()

    # Extract server name from user's input
    match_server_check = re.search(r'^!status\s+(\w+)$', p_message)

    # Extract server name and port number from the user's input
    match_port_check = re.search(r'^!status\s+(\w+)\s+(\d+)$', p_message)

    # If just status is invoked show full server list and statuses
    if p_message == '!status':

        base = ">>> ## Gigantic Server Status"

        for key, instance in servers.items():

            # Empty header here to avoid having it for each server
            status = StatusManager(instance, key, "")

            base += status.parse_current_status()

        return base

    # Shows a guide for user
    if p_message == '!status help':
        return ('>>> ### Gigantic Server Status Guide'
                '\n\nCommands are:'
                '\n\n`!status`: full server list'
                '\n`!status <server_name>`: to see the status for a specific server, for example`!status anhur`'
                '\n`!status <server_name> <instance_number>`: to see the status of a specific instance of a server, for example`!status syco 7777`'
                '\nAdd `?` at the beginning to send it to you via DM, for example `?!status skillz`')

    if match_port_check:
        server_name = match_port_check.group(1)
    else:
        server_name = match_server_check.group(1)

    # Check if the server is correct
    try:
        status_instance = StatusManager(servers.get(server_name), server_name)

    except KeyError:
        return f"{server_name} is not a valid server. Valid servers are: {servers.keys}"

    # If port check matches then return single instance return message
    if match_port_check:
        port = match_port_check.group(2)

        # Properly handle port errors
        try:
            return status_instance.check_port_status(port)

        except status_instance.InvalidPortError:
            return f"Invalid port {port} for server {server_name.capitalize()}. Valid ports are: {status_instance.server.udp_ports}"

    # If server check matches then return single server return message
    if match_server_check:
        return status_instance.parse_current_status()

    # Else if status command is invoked by user but parameters are invalid
    elif '!status' in p_message:
        return 'Invalid command. Use `!status help` to see see the guide'
