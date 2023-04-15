import socket

# Get the hostname of the local machine
hostname = socket.gethostname()

# Get the IP address associated with the hostname
ip_address = socket.gethostbyname(hostname)

# Print the current address
print("Current address:", ip_address)
