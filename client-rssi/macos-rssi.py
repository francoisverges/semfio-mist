#!/usr/bin/env python3

# Only for macOS use
# Display Wi-Fi stats from Wi-Fi NIC
# From @VergesFrancois

import os

# Executing the 'airport -I' command to retreive information on the current WLAN connection
stream = os.popen("airport -I")
lines = stream.read().split('\n')

# Extracting information out of the 'airport -I' command output
rssi = int(lines[0].split(": ")[1])
noise = int(lines[2].split(": ")[1])
SNR = rssi - noise
channel = int(lines[14].split(":")[1])
ssid = lines[12].split(": ")[1]
bssid = lines[11].split(": ")[1]

# Printing out the results
print(f"RSSI\t= {rssi} dBm")
print(f"Noise\t= {noise} dBm")
print(f"SNR\t= {SNR} dB")
print(f"Channel\t= {channel}")
print(f"SSID\t= {ssid}")
print(f"BSSID\t= {bssid}")
