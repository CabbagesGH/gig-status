import concurrent.futures
import re
from core import Server, StatusManager

# Define base servers
servers = {
    "cabbages": Server(),
    "skillz": Server(**{"url": "gig.illskillz.pro", "udp_ports": [7777]}),
    "anhur": Server(**{"url": "anhur.servegame.com", "flag": ":flag_us:", "code": "NA3"}),
    "syco": Server(**{
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

    # Extract server name (and port if added) from user's input
    match_status_check = re.search(r'^!status\s+(\w*)\s*(\S*)$', p_message)

    # If just status is invoked show full server list and statuses, threadpool used to speed up functions
    if p_message == '!status':

        base = ">>> ## Gigantic Server Status"

        with concurrent.futures.ThreadPoolExecutor() as executor:

            futures = [executor.submit(StatusManager.server_worker, instance, key) for key, instance in servers.items()]

            for future in concurrent.futures.as_completed(futures):
                base += future.result()

        return base

    # Shows a guide for user
    if p_message == '!status help':
        return ('>>> ### Gigantic Server Status Guide'
                '\n\nCommands are:'
                '\n\n`!status`: full server list'
                '\n`!status <server_name>`: to see the status for a specific server, for example `!status anhur`'
                '\n`!status <server_name> <instance_number>`: to see the status of a specific instance of a server, for example`!status syco 7777`'
                '\nAdd `?` at the beginning to send it to you via DM, for example `?!status skillz`')

    # Checks if message matches regex for single server or single port checking commands, and sets the server name
    if match_status_check:
        server_name = match_status_check.group(1)
    else:
        server_name = None

    # Check if the server is correct, and if correct check single server or single port
    if server_name:
        try:
            status_instance = StatusManager(servers[server_name], server_name)

            # If port check matches then return single instance return message
            if match_status_check.group(2):
                port = match_status_check.group(2)

                # Properly handle port errors
                try:
                    return status_instance.check_port_status(int(port))

                # If not an integer or if port doesn't match server lists
                except (ValueError, status_instance.InvalidPortError):
                    valid_udp_ports = ", ".join([str(port) for port in status_instance.server.udp_ports])
                    return f"Invalid port '{port}' for server {server_name.capitalize()}. Valid ports are: {valid_udp_ports}"

            # If server check matches then return single server return message
            else:
                return status_instance.parse_current_status()

        # If server check doesn't match then list valid servers
        except KeyError:
            valid_server_names = ", ".join([server for server in servers.keys()])
            return f"'{server_name}' is not a valid server. Valid servers are: {valid_server_names}"

    # Else if status command is invoked by user but parameters are invalid (checks for other common bot prefix)
    elif '!status' in p_message or '~status' in p_message:
        return 'Invalid command. Use `!status help` to see see the guide'
