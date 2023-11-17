#import requirement libraries
import os
import uuid
import time
import random
import json
import pycountry_convert as pc

#import web-based libraries
import html
import requests
import socket
import ipaddress
import ssl
import tldextract
import geoip2.database
import json
from dns import resolver, rdatatype

#import regex and encoding libraries
import re
import base64

# 检测base64合法性并解码
def is_valid_base64(string_value):
    try:
        # Decode the string using base64
        byte_decoded = base64.b64decode(string_value)
        # Encode the decoded bytes back to base64 and compare to the original string
        return base64.b64encode(byte_decoded).decode("utf-8") == string_value
    except:
        # If an exception is raised during decoding, the string is not valid base64
        return False

# 检测uuid合法性
def is_valid_uuid(value):
    try:
        # Try out to checkout valid UUID and return True
        uuid.UUID(str(value))
        return True
    except ValueError:
        # Return False If it's invalid
        return False

# 检测域名合法性
def is_valid_domain(hostname):
    # Extract the TLD, domain, and subdomain from the hostname
    ext = tldextract.extract(hostname)
    # Check if the domain and TLD are not empty
    return ext.domain != "" and ext.suffix != ""

# 检测IP合法性
def is_valid_ip_address(ip):
    try:
        # Try out to return True if it's IPV4 or IPV6
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        # Else it returns False
        return False

# 验证IPV6
def is_ipv6(ip):
    try:
        # Try out to return True if it's IPV6
        ipaddress.ip_address(ip)
        if ":" in ip:
            return True
        else:
            # Else it returns False
            return False
    except ValueError:
        return False

# ips解析
def get_ips(node):
    try:
        res = resolver.Resolver()
        res.nameservers = ["8.8.8.8"]

        # Retrieve IPV4 and IPV6
        answers_ipv4 = res.resolve(node, rdatatype.A, raise_on_no_answer=False)
        answers_ipv6 = res.resolve(node, rdatatype.AAAA, raise_on_no_answer=False)

        # Initialize set for IPV4 and IPV6
        ips = set()

        # Append IPV4 and IPV6 into set
        for rdata in answers_ipv4:
            ips.add(rdata.address)

        for rdata in answers_ipv6:
            ips.add(rdata.address)

        return ips
    except Exception:
        return None

# 返回域名的host
def get_ip(node):
    try:
        # Get node and return the current hostname
        return socket.gethostbyname(node)
    except Exception:
        return None

# 检查端口可用性
def check_port(ip, port, timeout=1):
    """
    Check if a port is open on a given IP address.

    Args:
    ip (str): The IP address.
    port (int): The port number.
    timeout (int, optional): The timeout in seconds. Defaults to 5.

    Returns:
    bool: True if the port is open, False otherwise.
    """
    try:
        sock = socket.create_connection(address=(ip, port), timeout=timeout)
        sock.close()
        print("Connection Port: Open".upper())
        return True
    except:
        print("Connection Port: Closed\n".upper())
        return False

# socket 测试端口ping延迟 vless+ws 的ping应小于timeout
def ping_ip_address(ip, port):
    try:
        ping_timeout = 25.00
        it = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port)) # connect_ex() 返回为0无异常
        ft = time.time()
        ping_time_test = (ft - it) * 1000
        sock.close()
        if result == 0:
            if ping_time_test < ping_timeout:
                return round((ft - it) * 1000, 1)
            else:
                return round(99, 1)
        else:
            return round(0, 1)
    except:
        return round(0, 1)



def check_modify_config(array_configuration, protocol_type, check_connection = True):
    # Initialize list for modified elements of configuration array
    modified_array = list()

    # Initialize array for security types of configuration
    tls_array = list()
    non_tls_array = list()

    # Initialize array for network types of configuration
    tcp_array = list()
    ws_array = list()
    

    if protocol_type == 'VLESS':
        for element in array_configuration:
            # Define VLESS protocol type pattern
            vless_pattern = r"vless://(?P<id>[^@]+)@\[?(?P<ip>[a-zA-Z0-9\.:\-:\_]+?)\]?:(?P<port>[0-9]+)/?\?(?P<params>[^#]+)#?(?P<title>(?<=#).*)?"

            # Print out original element
            print(f"ORIGINAL CONFIG: {element}")

            # Try out to match pattern and configuration
            vless_match = re.match(vless_pattern, element, flags=re.IGNORECASE)

            if vless_match is None:
                # Append no matches ShadowSocks into unmatched file
                with open("./splitted/no-match", "a") as no_match_file:
                    no_match_file.write(f"{element}\n")
                print("NO MATCH\n")
                # Continue for next element
                continue


            # Initialize dict to separate match groups by name capturing
            config = {
                "id": vless_match.group("id"),
                "ip": vless_match.group("ip"),
                "host": vless_match.group("ip"),
                "port": vless_match.group("port"),
                "params": vless_match.group("params"),
                "title": vless_match.group("title"),
            }
            
            # Checkout configuration UUID
            if not is_valid_uuid(config["id"]):
                print(f"INVALID UUID: {config['id']}\n")
                continue

            # Initialize set to append IP addresses
            ips_list = {config["ip"]}

            # Try out to retrieve config IP adresses if It's url link
            if not is_valid_ip_address(config["ip"]):
                ips_list = get_ips(config["ip"])

            # Continue for next element
            if ips_list is None:
                print("NO IP\n")
                continue


            # Split configuration parameters and initialize dict for parameters
            array_params_input = config["params"].split("&")
            dict_params = {}

            # Iterate over parameters and split based on key value
            for pair in array_params_input:
                try:
                    key, value = pair.split("=")
                    key = re.sub(r"servicename", "serviceName", re.sub(r"headertype", "headerType", re.sub(r"allowinsecure", "allowInsecure", key.lower()),),)
                    dict_params[key] = value
                except:
                    pass

            # Set parameters for servicename and allowinsecure keys
            if (dict_params.get("security", "") in ["tls"] and dict_params.get("sni", "") == "" and is_valid_domain(config["host"])):
                dict_params["sni"] = config["host"]
                dict_params["allowInsecure"] = 1

            # Ignore the configurations with specified security and None servicename
            if (dict_params.get("security", "") in ["tls"] and dict_params.get("sni", "") == ""):
                continue


            # Iterate over IP addresses to checkout connectivity
            for ip_address in ips_list:
                # Set config dict IP address
                config["ip"] = ip_address

                # Checkout IP address and port connectivity
                if check_connection:
                    if not check_port(config["ip"], int(config["port"])):
                        continue

                config_ping = ping_ip_address(config["ip"], int(config["port"]))

                time_out_bound = 99.0
                if config_ping == time_out_bound :
                    continue


                # Modify the IP address if it's IPV6
                if is_ipv6(config["ip"]):
                    config["ip"] = f"[{config['ip']}]"

                # Define configuration parameters string value and stripped based on & character
                config["params"] = f"security={dict_params.get('security', '')}&flow={dict_params.get('flow', '')}&sni={dict_params.get('sni', '')}&encryption={dict_params.get('encryption', '')}&type={dict_params.get('type', '')}&serviceName={dict_params.get('serviceName', '')}&host={dict_params.get('host', '')}&path={dict_params.get('path', '')}&headerType={dict_params.get('headerType', '')}&fp={dict_params.get('fp', '')}&pbk={dict_params.get('pbk', '')}&sid={dict_params.get('sid', '')}&alpn={dict_params.get('alpn', '')}&allowInsecure={dict_params.get('allowInsecure', '')}&"
                config["params"] = re.sub(r"\w+=&", "", config["params"])
                config["params"] = re.sub(r"(?:encryption=none&)|(?:headerType=none&)", "", config["params"], flags=re.IGNORECASE,)
                config["params"] = config["params"].strip("&")
                
                '''
                # Continue for next IP address if exists in modified array
                if any(f"vless://{config['id']}@{config['ip']}:{config['port']}?{config['params']}" in array_element for array_element in modified_array):
                    continue
                '''
                # Retrieve config network type and security type
                config_type = dict_params.get('type', 'TCP').upper() if dict_params.get('type') not in [None, ''] else 'TCP'
                config_secrt = dict_params.get('security','NA').upper() if dict_params.get('security') not in [None, ''] else 'NA'
                if config_secrt == 'REALITY':
                    config_secrt = 'RLT'

                # Modify configuration title based on server and protocol properties
                config["title"] = f"\U0001F512 VL-{config_type}-{config_secrt} {config['ip']}:{config['port']} \U0001F4E1 PING-{config_ping:04.1f}-MS"

                # Print out modified configuration
                print(f"MODIFIED CONFIG: vless://{config['id']}@{config['ip']}:{config['port']}?{config['params']}#{config['title']}\n")
                
                # Append modified configuration into modified array
                modified_array.append(f"vless://{config['id']}@{config['ip']}:{config['port']}?{config['params']}#{config['title']}")

                # Append security type array
                if config_secrt == 'TLS' :
                    tls_array.append(f"vless://{config['id']}@{config['ip']}:{config['port']}?{config['params']}#{config['title']}")
                elif config_secrt == 'NA':
                    non_tls_array.append(f"vless://{config['id']}@{config['ip']}:{config['port']}?{config['params']}#{config['title']}")

                # Append network type array
                if config_type == 'TCP':
                    tcp_array.append(f"vless://{config['id']}@{config['ip']}:{config['port']}?{config['params']}#{config['title']}")
                elif config_type == 'WS':
                    ws_array.append(f"vless://{config['id']}@{config['ip']}:{config['port']}?{config['params']}#{config['title']}")


    elif protocol_type == 'TUIC':
        for element in array_configuration:
            # Define ShadowSocks protocol type pattern
            tuic_pattern = r"tuic://(?P<id>[^:]+):(?P<pass>[^@]+)@\[?(?P<ip>[a-zA-Z0-9\.:-]+?)\]?:(?P<port>[0-9]+)/?\?(?P<params>[^#]+)#?(?P<title>(?<=#).*)?"

            # Print out original element
            print(f"ORIGINAL CONFIG: {element}")

            # Try out to match pattern and configuration
            tuic_match = re.match(tuic_pattern, element, flags=re.IGNORECASE)

            if tuic_match is None:
                # Append no matches ShadowSocks into unmatched file
                with open("./splitted/no-match", "a") as no_match_file:
                    no_match_file.write(f"{element}\n")
                print("NO MATCH\n")
                # Continue for next element
                continue


            # Initialize dict to separate match groups by name capturing
            config = {
                "id": tuic_match.group("id"),
                "pass": tuic_match.group("pass"),
                "ip": tuic_match.group("ip"),
                "port": tuic_match.group("port"),
                "params": tuic_match.group("params"),
                "title": tuic_match.group("title")
            }

            # Checkout configuration UUID
            if not is_valid_uuid(config["id"]):
                print(f"INVALID UUID: {config['id']}\n")
                continue

            # Initialize set to append IP addresses
            ips_list = {config["ip"]}

            # Try out to retrieve config IP adresses if It's url link
            if not is_valid_ip_address(config["ip"]):
                ips_list = get_ips(config["ip"])

            # Continue for next element
            if ips_list is None:
                print("NO IP\n")
                continue


            # Iterate over IP addresses to checkout connectivity
            for ip_address in ips_list:
                # Set config dict IP address
                config["ip"] = ip_address

                # Checkout IP address and port connectivity
                if check_connection:
                    if not check_port(config["ip"], int(config["port"])):
                        continue

                config_ping = ping_ip_address(config["ip"], int(config["port"]))


                # Modify the IP address if it's IPV6
                if is_ipv6(config["ip"]):
                    config["ip"] = f"[{config['ip']}]"


                # Modify configuration title based on server and protocol properties
                config["title"] = f"\U0001F512 TUIC-UDP {config['ip']}:{config['port']} \U0001F4E1 PING-{config_ping:04.1f}-MS"

                # Print out modified configuration
                print(f"MODIFIED CONFIG: tuic://{config['id']}:{config['pass']}@{config['ip']}:{config['port']}?{config['params']}#{config['title']}\n")

                # Append modified configuration into modified array
                modified_array.append(f"tuic://{config['id']}:{config['pass']}@{config['ip']}:{config['port']}?{config['params']}#{config['title']}")



    elif protocol_type == 'HYSTERIA':
        for element in array_configuration:
            if element.startswith('hysteria'):
                # Define ShadowSocks protocol type pattern
                hysteria_1_pattern = r"hysteria://\[?(?P<ip>[a-zA-Z0-9\.:-]+?)\]?:(?P<port>[0-9]+)/?\?(?P<params>[^#]+)#?(?P<title>(?<=#).*)?"

                # Print out original element
                print(f"ORIGINAL CONFIG: {element}")

                # Try out to match pattern and configuration
                hysteria_match = re.match(hysteria_1_pattern, element, flags=re.IGNORECASE)

                if hysteria_match is None:
                    # Append no matches ShadowSocks into unmatched file
                    with open("./splitted/no-match", "a") as no_match_file:
                        no_match_file.write(f"{element}\n")
                    print("NO MATCH\n")
                    # Continue for next element
                    continue


                # Initialize dict to separate match groups by name capturing
                config = {
                    "ip": hysteria_match.group("ip"),
                    "port": hysteria_match.group("port"),
                    "params": hysteria_match.group("params"),
                    "title": hysteria_match.group("title")
                }


                # Initialize set to append IP addresses
                ips_list = {config["ip"]}

                # Try out to retrieve config IP adresses if It's url link
                if not is_valid_ip_address(config["ip"]):
                    ips_list = get_ips(config["ip"])

                # Continue for next element
                if ips_list is None:
                    print("NO IP\n")
                    continue


                # Iterate over IP addresses to checkout connectivity
                for ip_address in ips_list:
                    # Set config dict IP address
                    config["ip"] = ip_address

                    # Checkout IP address and port connectivity
                    if check_connection:
                        if not check_port(config["ip"], int(config["port"])):
                            continue

                    config_ping = ping_ip_address(config["ip"], int(config["port"]))


                    # Modify the IP address if it's IPV6
                    if is_ipv6(config["ip"]):
                        config["ip"] = f"[{config['ip']}]"


                    # Modify configuration title based on server and protocol properties
                    config["title"] = f"\U0001F512 HYSTERIA-UDP {config['ip']}:{config['port']} \U0001F4E1 PING-{config_ping:04.1f}-MS"

                    # Print out modified configuration
                    print(f"MODIFIED CONFIG: hysteria://{config['ip']}:{config['port']}?{config['params']}#{config['title']}\n")

                    # Append modified configuration into modified array
                    modified_array.append(f"hysteria://{config['ip']}:{config['port']}?{config['params']}#{config['title']}")


            elif element.startswith('hy2'):
                # Define ShadowSocks protocol type pattern
                hysteria_2_pattern = r"hy2://(?P<pass>[^@]+)@\[?(?P<ip>[a-zA-Z0-9\.:-]+?)\]?:(?P<port>[0-9]+)/?\?(?P<params>[^#]+)#?(?P<title>(?<=#).*)?"

                # Print out original element
                print(f"ORIGINAL CONFIG: {element}")

                # Try out to match pattern and configuration
                hysteria_match = re.match(hysteria_2_pattern, element, flags=re.IGNORECASE)

                if hysteria_match is None:
                    # Append no matches ShadowSocks into unmatched file
                    with open("./splitted/no-match", "a") as no_match_file:
                        no_match_file.write(f"{element}\n")
                    print("NO MATCH\n")
                    # Continue for next element
                    continue


                # Initialize dict to separate match groups by name capturing
                config = {
                    "pass": hysteria_match.group("pass"),
                    "ip": hysteria_match.group("ip"),
                    "port": hysteria_match.group("port"),
                    "params": hysteria_match.group("params"),
                    "title": hysteria_match.group("title")
                }


                # Initialize set to append IP addresses
                ips_list = {config["ip"]}

                # Try out to retrieve config IP adresses if It's url link
                if not is_valid_ip_address(config["ip"]):
                    ips_list = get_ips(config["ip"])

                # Continue for next element
                if ips_list is None:
                    print("NO IP\n")
                    continue


                # Iterate over IP addresses to checkout connectivity
                for ip_address in ips_list:
                    # Set config dict IP address
                    config["ip"] = ip_address

                    # Checkout IP address and port connectivity
                    if check_connection:
                        if not check_port(config["ip"], int(config["port"])):
                            continue

                    config_ping = ping_ip_address(config["ip"], int(config["port"]))


                    # Modify the IP address if it's IPV6
                    if is_ipv6(config["ip"]):
                        config["ip"] = f"[{config['ip']}]"


                    # Modify configuration title based on server and protocol properties
                    config["title"] = f"\U0001F512 HYSTERIA-UDP {config['ip']}:{config['port']} \U0001F4E1 PING-{config_ping:04.1f}-MS"

                    # Print out modified configuration
                    print(f"MODIFIED CONFIG: hy2://{config['pass']}@{config['ip']}:{config['port']}?{config['params']}#{config['title']}\n")

                    # Append modified configuration into modified array
                    modified_array.append(f"hy2://{config['pass']}@{config['ip']}:{config['port']}?{config['params']}#{config['title']}")                

    else:
        modified_array = array_configuration

    return modified_array, tls_array, non_tls_array, tcp_array, ws_array


def config_sort(array_configuration, bound_ping = 25):
    # Initialize list for sorted configs
    sort_init_list = list()

    for config in array_configuration:
        if config.startswith('vless') :
            ping_time = float(config.split(' ')[-1].split('-')[1])
            ping_config_tp = (ping_time, config)
            sort_init_list.append(ping_config_tp)

    # Iterate over array configuration to separate configurations
    forward_sorted_list = [(ping, config) for ping, config in sort_init_list if ping >= bound_ping]
    reversed_sorted_list = [(ping, config) for ping, config in sort_init_list if ping < bound_ping]

    # Sort configurations based on ping on forawarded and reversed
    forward_sorted_list = [config for ping, config in sorted(forward_sorted_list, key = lambda element: element[0])]
    reversed_sorted_list = [config for ping, config in sorted(reversed_sorted_list, key = lambda element: element[0], reverse = True)]

    forward_sorted_list.extend(reversed_sorted_list)
    array_configuration = forward_sorted_list

    return array_configuration


def create_internet_protocol(array_configuration):
    # Initialize list for sorted configs
    internet_protocol_ver4 = list()
    internet_protocol_ver6 = list()

    for config in array_configuration:
        if config.startswith('vless') :
            ip_port = config.split(' ')[-3].split('-')[-1]
            if '[' in ip_port or ']' in ip_port:
                internet_protocol_ver6.append(config)
            else:
                internet_protocol_ver4.append(config)


    return internet_protocol_ver4, internet_protocol_ver6
