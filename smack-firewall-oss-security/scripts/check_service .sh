#!/bin/sh
echo "=== Checking insecure services (telnet, ftp, rsh, etc.) ==="

services="telnet ftp rsh rexec rlogin nfs"

for srv in $services; do
    systemctl list-units --type=service | grep -iq "$srv"
    if [ $? -eq 0 ]; then
        echo "[WARN] $srv service is running"
    else
        echo "[OK] $srv service is not running"
    fi
done
