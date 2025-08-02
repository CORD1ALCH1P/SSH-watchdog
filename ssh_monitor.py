import time
import re
import requests
from datetime import datetime

# configuration
TOKEN = '123456789:ABCDEF_your_token_here'
CHAT_ID = 'exmp_your_chat_id_here'
LOG_FILE = '/var/log/auth.log'  # Or /var/log/secure for CentOS

# Telegram sending
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    requests.post(url, data=data)

# log real-time reading
def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line

# pars log's string
def parse_ssh_log(line):
    now = datetime.now().strftime('%H:%M:%S')

    # if pass was accepted
    match_accepted = re.search(r'Accepted \S+ for (\S+) from ([\d.]+) port (\d+)', line)
    if match_accepted:
        user, ip, port = match_accepted.groups()
        return f"✅ Accepted password for <b>{user}</b> from <code>{ip}</code> port <code>{port}</code> ssh2 at <b>{now}</b>"

    # if pass was wrong
    match_failed = re.search(r'Failed \S+ for (invalid user )?(\S+) from ([\d.]+) port (\d+)', line)
    if match_failed:
        _, user, ip, port = match_failed.groups()
        return f"❌ Failed password for <b>{user}</b> from <code>{ip}</code> port <code>{port}</code> ssh2 at <b>{now}</b>"

    return None

# main
with open(LOG_FILE, 'r') as logfile:
    loglines = follow(logfile)
    for line in loglines:
        if 'sshd' not in line:
            continue
        message = parse_ssh_log(line)
        if message:
            send_telegram_message(message)
