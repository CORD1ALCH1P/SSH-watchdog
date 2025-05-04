## 🔐 SSH Login Monitor with Telegram Alerts

A simple Python-based tool that monitors SSH login attempts on a Linux server and sends real-time notifications to a Telegram bot. Useful for system administrators who want to stay informed about access activity on their systems — both successful and failed login attempts.

---

### 📆 Features

* ✅ **Real-time monitoring** of `/var/log/auth.log` (or `/var/log/secure`)
* 📲 **Telegram notifications** for:

  * Successful SSH logins
  * Failed login attempts
* 📌 Includes:

  * Username
  * IP address
  * Port
  * Time of the event
* 🔐 Detects both normal and invalid users

---

### 📋 Example Telegram Message

```
✅ Accepted password for root from 192.168.1.100 port 55221 ssh2 at 17:23:45
❌ Failed password for admin from 203.0.113.55 port 60001 ssh2 at 17:24:05
```

---

### 🚀 Setup Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/CORD1ALCH1P/SSH-watchdog.git
```

#### 2. Install Required Packages

```bash
pip install requests
```

#### 3. Create a Telegram Bot

* Talk to [@BotFather](https://t.me/BotFather) on Telegram
* Use `/newbot` to create a new bot and get the **API token**
* Start a chat with your bot to activate it
* Use `getUpdates` or [this tool](https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates) to get your `chat_id`

#### 4. Configure the Script

Edit `ssh_monitor.py` and replace:

```python
TOKEN = 'your_bot_token'
CHAT_ID = 'your_chat_id'
```

#### 5. (Optional) Set Up as a Systemd Service

Create a file `/etc/systemd/system/ssh_monitor.service`:

```ini
[Unit]
Description=SSH Monitor with Telegram Alerts
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/ssh_monitor.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target
```

Then run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ssh_monitor.service
sudo systemctl start ssh_monitor.service
```

---

### 📝 Notes

* Works on most Linux distributions.
* Default log file path is `/var/log/auth.log` (Debian/Ubuntu). On RHEL/CentOS use `/var/log/secure`.
* The script assumes `systemd` for service management (optional).

---

### ❗ Security Disclaimer

This script provides **monitoring and alerting only**. It does not prevent intrusions or implement rate limiting or bans. For real protection, consider using tools like `fail2ban`, SSH key authentication, and firewall rules.

---
