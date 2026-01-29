import subprocess
import shlex
import socket
import json
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
LAST_SEEN = SCRIPT_DIR / 'logs' / 'last_seen.json'
UPTIME = SCRIPT_DIR / 'logs' / 'uptime.json'


def safe_load_json(p: Path):
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


def safe_write_json(p: Path, data):
    p.write_text(json.dumps(data, indent=2))


def ping_check(ip, retries=4, timeout=1):
    if not ip:
        return False, 'no-ip'

    for i in range(retries):
        cmd = f"ping -c 1 -W {timeout} {ip}"
        try:
            p = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, timeout=timeout+2)
            if p.returncode == 0:
                return True, ''
        except subprocess.TimeoutExpired:
            pass
        
    return False, f'ping_failed_{retries}'


def ssh_check(ip, retries=4, timeout=1):
    if not ip:
        return False, 'no-ip'

    for i in range(retries):
        try:
            sock = socket.create_connection((ip, 22), timeout=timeout)
            sock.close()
            return True, ''
        except Exception:
            pass
        
    return False, f'ssh_failed_{retries}'


def update_status_files(name, ip, is_up):
    last_seen = safe_load_json(LAST_SEEN)
    uptime = safe_load_json(UPTIME)

    now = datetime.now().isoformat(sep=' ', timespec='seconds')

    if name not in last_seen:
        last_seen[name] = None
    if name not in uptime:
        uptime[name] = {'up': 0, 'down': 0}

    if is_up:
        last_seen[name] = now
        uptime[name]['up'] += 1
    else:
        uptime[name]['down'] += 1

    safe_write_json(LAST_SEEN, last_seen)
    safe_write_json(UPTIME, uptime)

    return last_seen[name] or '-', f"UP:{uptime[name]['up']} DOWN:{uptime[name]['down']}"


