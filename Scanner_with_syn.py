import socket
import threading
import time
from scapy.all import *
from ipaddress import ip_network
import sys

def is_host_alive(target):
    try:
        ip = socket.gethostbyname(target)
        return True
    except socket.gaierror:
        return False

def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((ip, port))
        banner = s.recv(1024)
        return banner.decode().strip()
    except:
        return None

def syn_scan(target, port):
    src_port = RandShort()
    try:
        p = sr1(IP(dst=target)/TCP(sport=src_port,dport=port,flags="S"), timeout=1, verbose=0)
        if p:
            if p[TCP].flags == "SA":
                send(IP(dst=target)/TCP(sport=src_port,dport=port,flags="R"), verbose=0)
                return True
        return False
    except:
        return False

def scan_port(target, port, scan_type, open_ports, rate_limit):
    if rate_limit:
        time.sleep(rate_limit)
    if scan_type == "syn":
        if syn_scan(target, port):
            banner = grab_banner(target, port)
            if banner:
                open_ports[port] = banner
            else:
                open_ports[port] = None
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            banner = grab_banner(target, port)
            if banner:
                open_ports[port] = banner
            else:
                open_ports[port] = None
        s.close()

def print_progress_bar(completed, total, length=50):
    progress = int((completed / total) * length)
    bar = f"[{'#' * progress}{'.' * (length - progress)}] {completed}/{total} Ports Scanned"
    sys.stdout.write("\r" + bar)
    sys.stdout.flush()

def main():
    target_input = input("Enter the target (IP/Hostname/Subnet): ")
    
    if '/' in target_input:
        targets = [str(ip) for ip in ip_network(target_input)]
    else:
        targets = [target_input]

    scan_type = input("Select scan type (connect/syn): ").lower()
    start_port = int(input("Enter the start port: "))
    end_port = int(input("Enter the end port: "))
    rate_limit = float(input("Enter rate limit (seconds between scans, 0 for no limit): "))

    for target in targets:
        if not is_host_alive(target):
            print(f"Unable to reach {target}. Skipping.")
            continue

        threads = []
        open_ports = {}
        scanned_ports = 0

        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=scan_port, args=(target, port, scan_type, open_ports, rate_limit))
            threads.append(thread)
            thread.start()
            thread.join()  
            scanned_ports += 1
            print_progress_bar(scanned_ports, end_port - start_port + 1)

        print(f"\nScanning {target} complete!")
        if open_ports:
            print(f"Open ports on {target}:")
            for port, banner in open_ports.items():
                if banner:
                    print(f"{port}: {banner}")
                else:
                    print(f"{port}")
        else:
            print(f"No open ports on {target} in the range {start_port}-{end_port}.")

if __name__ == "__main__":
    main()
