import socket

# Get internal IP address
hostname = socket.gethostname()
internal_ip = socket.gethostbyname(hostname)
print("Internal IP address:", internal_ip)

# Get external IP address
external_ip = socket.get('https://api.ipify.org').text
print("External IP address:", external_ip)

