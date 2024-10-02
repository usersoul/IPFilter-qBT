import re
import ipaddress
import requests
from requests.exceptions import RequestException

def convert_ipv6(ip):
    return ipaddress.IPv6Address(ip).exploded

def process_ip_list(ip_list):
    processed = []
    for line in ip_list:
        line = line.strip()
        if re.match(r'^(\d{1,3}\.){3}\d{1,3}(/\d{1,2})?$', line):  # IPv4
            try:
                if '/' in line:  # CIDR notation
                    network = ipaddress.IPv4Network(line, strict=False)
                    processed.append(f"{network.network_address + 1}-{network.broadcast_address - 1}")
                else:
                    processed.append(line)
            except ValueError:
                pass  # Skip invalid IPv4 addresses
        elif ':' in line:  # IPv6
            try:
                if '/' in line:  # CIDR notation
                    network = ipaddress.IPv6Network(line, strict=False)
                    processed.append(f"{convert_ipv6(network.network_address)}-{convert_ipv6(network.broadcast_address)}")
                else:
                    processed.append(convert_ipv6(line))
            except ipaddress.AddressValueError:
                pass  # Skip invalid IPv6 addresses
    return processed

def fetch_ip_list(urls):
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text.splitlines()
        except RequestException as e:
            print(f"Error fetching from {url}: {e}")
    raise Exception("Failed to fetch IP list from all provided URLs")

def main():
    urls = [
        "https://raw.githubusercontent.com/PBH-BTN/BTN-Collected-Rules/main/combine/all.txt",
        "https://bcr.pbh-btn.ghorg.ghostchu-services.top/combine/all.txt",
        "https://fastly.jsdelivr.net/gh/PBH-BTN/BTN-Collected-Rules@master/combine/all.txt"
    ]
    output_filename = 'ipfilter.dat'

    try:
        ip_list = fetch_ip_list(urls)
        filtered_ips = process_ip_list(ip_list)

        with open(output_filename, 'w', encoding='utf-8') as f:
            for ip in filtered_ips:
                f.write(f"{ip}\n")

        print(f"IP filter file has been created as '{output_filename}'")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()