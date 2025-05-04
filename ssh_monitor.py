import time
import re
import requests
from datetime import datetime

# Настройки
TOKEN = '123456789:ABCDEF_your_token_here'
CHAT_ID = '1079869451_your_chat_id_here'
LOG_FILE = '/var/log/auth.log'  # Или /var/log/secure на CentOS

# Отправка сообщения в Telegram
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    requests.post(url, data=data)

# Чтение лога в реальном времени
def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line

# Парсинг строки лога
def parse_ssh_log(line):
    now = datetime.now().strftime('%H:%M:%S')

    # Успешный вход
    match_accepted = re.search(r'Accepted \S+ for (\S+) from ([\d.]+) port (\d+)', line)
    if match_accepted:
        user, ip, port = match_accepted.groups()
        return f"✅ Accepted password for <b>{user}</b> from <code>{ip}</code> port <code>{port}</code> ssh2 at <b>{now}</b>"

    # Неудачный вход
    match_failed = re.search(r'Failed \S+ for (invalid user )?(\S+) from ([\d.]+) port (\d+)', line)
    if match_failed:
        _, user, ip, port = match_failed.groups()
        return f"❌ Failed password for <b>{user}</b> from <code>{ip}</code> port <code>{port}</code> ssh2 at <b>{now}</b>"

    return None

# Основной цикл
with open(LOG_FILE, 'r') as logfile:
    loglines = follow(logfile)
    for line in loglines:
        if 'sshd' not in line:
            continue
        message = parse_ssh_log(line)
        if message:
            send_telegram_message(message)
