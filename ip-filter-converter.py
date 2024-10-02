import re
import ipaddress

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

def main():
    input_filename = input("Please enter the name of your IP list file (e.g., ip_list.txt): ")
    output_filename = 'ipfilter.dat'

    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            ip_list = [line.strip() for line in f if line.strip()]

        filtered_ips = process_ip_list(ip_list)

        with open(output_filename, 'w', encoding='utf-8') as f:
            for ip in filtered_ips:
                f.write(f"{ip}\n")

        print(f"IP filter file has been created as '{output_filename}'")

    except FileNotFoundError:
        print(f"Error: The input file '{input_filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()