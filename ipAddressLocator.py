import re
import socket
import requests
import platform
import subprocess

def get_local_ip():
    """Kunin ang local IP address ng device."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except socket.error:
        return "❌ Failed to retrieve local IP"

def get_public_ip():
    """Kunin ang public IP address ng device."""
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        return response.json()["ip"]
    except requests.RequestException:
        return "❌ Failed to retrieve public IP"

def get_ip_location(ip):
    """Kunin ang geolocation details ng isang Public IP address gamit ang ip-api.com."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data["status"] == "success":
            return {
                "Country": data["country"],
                "Region": data["regionName"],
                "City": data["city"],
                "ISP": data["isp"],
                "Latitude": data["lat"],
                "Longitude": data["lon"]
            }
        else:
            return {"Error": "Invalid IP or API issue"}
    except requests.RequestException:
        return {"Error": "Failed to connect to IP API"}

def is_private_ip(ip):
    """I-check kung ang IP ay private/local (hindi public)."""
    private_ip_patterns = [
        re.compile(r"^10\."),
        re.compile(r"^192\.168\."),
        re.compile(r"^172\.(1[6-9]|2[0-9]|3[0-1])\."),
    ]
    return any(pattern.match(ip) for pattern in private_ip_patterns)

def get_mac_address(ip):
    """Kunin ang MAC address ng isang local IP address (Windows/Linux)."""
    try:
        os_type = platform.system()
        if os_type == "Windows":
            result = subprocess.check_output(f"arp -a {ip}", shell=True, text=True)
        elif os_type == "Linux" or os_type == "Darwin":
            result = subprocess.check_output(f"arp -n {ip}", shell=True, text=True)
        else:
            return "❌ Unsupported OS for MAC retrieval"

        match = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", result)
        return match.group(0) if match else "❌ MAC Address Not Found"
    except subprocess.SubprocessError:
        return "❌ Failed to retrieve MAC Address"
    
def scan_local_network():
    """I-scan ang local network para makita ang ibang devices (Gamit ang arp -a)."""
    try:
        os_type = platform.system()
        if os_type == "Windows":
            result = subprocess.check_output("arp -a", shell=True, text=True)
        elif os_type == "Linux" or os_type == "Darwin":
            result = subprocess.check_output("arp -n", shell=True, text=True)
        else:
            return "❌ Unsupported OS for network scanning"
        return result
    except subprocess.SubprocessError:
        return "❌ Failed to scan local network"

if __name__ == "__main__":
    print("🔍 IP Address Tool\n")
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    print(f"🖥 Local IP Address: {local_ip}")
    print(f"🌍 Public IP Address: {public_ip}")
    target_ip = input("\n🔹 Enter an IP Address to locate (or press Enter to use your public IP): ").strip()
    if not target_ip:
        target_ip = public_ip

    print(f"\n📍 Checking Details for {target_ip}:")
    if is_private_ip(target_ip):
        print("   🔹 Detected as LOCAL IP Address")
        mac_address = get_mac_address(target_ip)
        print(f"   🏠 Device MAC Address: {mac_address}")
    else:
        print("   🔹 Detected as PUBLIC IP Address")
        location = get_ip_location(target_ip)
        for key, value in location.items():
            print(f"   {key}: {value}")
    print("\n🔎 Scanning Local Network...\n")
    network_scan_result = scan_local_network()
    print(network_scan_result)
