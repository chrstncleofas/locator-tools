import socket
import requests
import phonenumbers
from phonenumbers import geocoder, carrier

def get_local_ip():
    """Kunin ang local IP address ng device."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except socket.error:
        return "Failed to retrieve local IP"

def get_public_ip():
    """Kunin ang public IP address ng device."""
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        return response.json().get("ip", "Failed to retrieve public IP")
    except requests.RequestException:
        return "Failed to retrieve public IP"

def get_ip_location(ip):
    """Kunin ang geolocation details ng isang IP address gamit ang ip-api.com."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data.get("status") == "success":
            return {
                "Country": data.get("country"),
                "Region": data.get("regionName"),
                "City": data.get("city"),
                "ISP": data.get("isp"),
                "Latitude": data.get("lat"),
                "Longitude": data.get("lon")
            }
        else:
            return {"Error": "Invalid IP or API issue"}
    except requests.RequestException:
        return {"Error": "Failed to connect to IP API"}

def get_mobile_location(number):
    """Kunin ang geolocation ng isang mobile number (Country, Carrier)."""
    try:
        parsed_number = phonenumbers.parse(number)
        country = geocoder.description_for_number(parsed_number, "en")
        carrier_name = carrier.name_for_number(parsed_number, "en")

        return {
            "Country": country,
            "Carrier": carrier_name,
        }
    except phonenumbers.NumberParseException:
        return {"Error": "Invalid phone number format"}

if __name__ == "__main__":
    print("\n🔍 IP & Mobile Tracker Tool")
    print("1️⃣ Get Local & Public IP")
    print("2️⃣ Get IP Location")
    print("3️⃣ Track Mobile Number with Custom IP")
    print("0️⃣ Exit")
    
    choice = input("\nEnter your choice: ")
    
    if choice == "1":
        local_ip = get_local_ip()
        public_ip = get_public_ip()
        print(f"\n🖥 Local IP Address: {local_ip}")
        print(f"🌍 Public IP Address: {public_ip}")
    
    elif choice == "2":
        target_ip = input("\n🔹 Enter an IP Address to locate: ").strip()
        location = get_ip_location(target_ip)
        print("\n📍 Geolocation Data:")
        for key, value in location.items():
            print(f"   {key}: {value}")
    
    elif choice == "3":
        mobile_number = input("\n📞 Enter a mobile number with country code (e.g., +639123456789): ").strip()
        mobile_location = get_mobile_location(mobile_number)

        print("\n📍 Mobile Number Details:")
        for key, value in mobile_location.items():
            print(f"   {key}: {value}")

        custom_ip = input("\n🌍 (Optional) Enter an IP Address to locate: ").strip()
        if custom_ip:
            ip_location = get_ip_location(custom_ip)
            print("\n📍 IP Address Details:")
            for key, value in ip_location.items():
                print(f"   {key}: {value}")
    
    elif choice == "0":
        print("\n👋 Exiting...")
    else:
        print("\n❌ Invalid choice. Please try again.")
