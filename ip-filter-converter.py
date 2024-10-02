import re
import ipaddress

def convert_ipv6(ip):
    # Convert IPv6 to full form
    return ipaddress.IPv6Address(ip).exploded

def process_ip_list(ip_list):
    processed = []
    for line in ip_list:
        line = line.strip()
        if re.match(r'^(\d{1,3}\.){3}\d{1,3}(/\d{1,2})?$', line):  # IPv4
            processed.append(line)
        elif ':' in line:  # IPv6
            try:
                if '/' in line:  # CIDR notation
                    network = ipaddress.IPv6Network(line, strict=False)
                    processed.append(f"[{convert_ipv6(network.network_address)}] - [{convert_ipv6(network.broadcast_address)}]")
                else:
                    processed.append(f"[{convert_ipv6(line)}]")
            except ipaddress.AddressValueError:
                pass  # Skip invalid IPv6 addresses
    return processed

# Read the input
ip_list = [line.strip() for line in input_text.split('\n') if line.strip()]

# Process the IP list
filtered_ips = process_ip_list(ip_list)

# Write to ipfilter.dat
with open('ipfilter.dat', 'w', encoding='utf-8') as f:
    for ip in filtered_ips:
        f.write(f"{ip}\n")

print("IP filter file has been created as 'ipfilter.dat'")
