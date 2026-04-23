# WiFi Crasher

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-2ea44f)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20WSL2-0366d6)
![Status](https://img.shields.io/badge/Status-Active-success)

**Wireless security auditing utility for controlled, authorized environments**

[Overview](#overview) • [Features](#features) • [Requirements](#requirements) • [Installation](#installation) • [Usage](#usage) • [Safety and Legal](#safety-and-legal)

</div>

---

<div align="center">
	<img src="pic.png" alt="WiFi Crasher interface screenshot" width="900">
</div>

## Overview

WiFi Crasher is a Python-based CLI tool built for wireless security testing and lab validation. It streamlines common workflows around:

- Discovering nearby access points
- Inspecting signal quality
- Preparing monitor mode for testing
- Running deauthentication tests as part of authorized assessments

The tool uses the `aircrack-ng` ecosystem under the hood and is intended for security researchers, students, and network administrators.

## Features

- Automatic wireless interface detection
- Live network scan with signal strength indicators
- Guided target selection in terminal menus
- Monitor mode setup with conflict handling
- Deauthentication testing workflow
- Session-friendly output and CSV backup behavior

## Requirements

### Hardware

- WiFi adapter with monitor mode support
- WiFi adapter with packet injection support
- 2 GB RAM minimum
- 100 MB free disk space

### Software

- Python 3.8+
- `aircrack-ng`
- `iw`
- `rfkill`
- `wireless-tools`

Notes:

- Linux is the recommended environment.
- On Windows, run via WSL2 for best compatibility.
- Native Windows wireless driver limitations may prevent full functionality.

## Installation

### Linux (Ubuntu, Debian, Kali, Zorin)

```bash
sudo apt update
sudo apt install -y python3 python3-pip aircrack-ng wireless-tools iw rfkill

git clone https://github.com/squidward404/wifi-crasher.git
cd wifi-crasher

# optional
chmod +x wifi-crasher.py
```

### macOS

```bash
# install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install python3 aircrack-ng

git clone https://github.com/squidward404/wifi-crasher.git
cd wifi-crasher
```

### Windows (Recommended: WSL2)

```bash
# run in PowerShell (Administrator)
wsl --install

# then inside your WSL distro
sudo apt update
sudo apt install -y python3 python3-pip aircrack-ng wireless-tools iw rfkill

git clone https://github.com/squidward404/wifi-crasher.git
cd wifi-crasher
```

## Usage

```bash
cd wifi-crasher
sudo rfkill unblock all
sudo python3 wifi-crasher.py
```

## Safety and Legal

This project is provided for education and authorized security testing only.

You must test only networks that:

- You own, or
- You have explicit written permission to assess

Unauthorized wireless testing can violate local laws and regulations. You are solely responsible for how you use this software.

## Contributing

Issues and pull requests are welcome. If you are reporting a bug, include:

- Operating system and version
- Wireless adapter model
- Steps to reproduce
- Relevant terminal output

## License

Released under the MIT License.
