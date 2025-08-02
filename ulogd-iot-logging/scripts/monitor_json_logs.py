#!/usr/bin/env python3

import json
import time
import os

LOG_FILE = "/var/log/firewall_log.json"

def tail_f(file_path):
    """Generator that yields new lines as they are written to the log file."""
    with open(file_path, 'r') as f:
        f.seek(0, os.SEEK_END)  # Move to the end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line

def parse_and_display(line):
    try:
        log_entry = json.loads(line)
        timestamp = log_entry.get("timestamp", "N/A")
        verdict = log_entry.get("verdict", "N/A")
        src_ip = log_entry.get("ip", {}).get("saddr", "N/A")
        dst_ip = log_entry.get("ip", {}).get("daddr", "N/A")
        proto = log_entry.get("ip", {}).get("protocol", "N/A")
        sport = log_entry.get("tcp", {}).get("sport", "N/A")
        dport = log_entry.get("tcp", {}).get("dport", "N/A")
        print(f"[{timestamp}] {verdict} {proto} {src_ip}:{sport} → {dst_ip}:{dport}")
    except json.JSONDecodeError:
        print("[!] Malformed JSON line.")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")

def main():
    print(f"[+] Monitoring JSON log: {LOG_FILE}")
    if not os.path.exists(LOG_FILE):
        print(f"[!] File does not exist: {LOG_FILE}")
        return

    for line in tail_f(LOG_FILE):
        parse_and_display(line)

if __name__ == "__main__":
    main()
