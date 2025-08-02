#!/bin/bash

# Description:
# Manual log rotation script for ULOGD logs
# Use this when logrotate is not set up or for testing purposes

LOG_FILES=(
    "/var/log/ulogd.log"
    "/var/log/full.log"
    "/var/log/firewall_log.json"
    "/var/log/ulogd/custom.log"
)
XML_LOG_DIR="/var/log/ulogd_xml"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo "[+] Starting manual log rotation at $TIMESTAMP"

for FILE in "${LOG_FILES[@]}"; do
    if [ -f "$FILE" ]; then
        mv "$FILE" "$FILE.$TIMESTAMP"
        echo "  --> Rotated: $FILE → $FILE.$TIMESTAMP"
        touch "$FILE"
    else
        echo "  [!] Skipping: $FILE does not exist"
    fi
done

# Rotate XML logs if directory exists
if [ -d "$XML_LOG_DIR" ]; then
    for XMLFILE in "$XML_LOG_DIR"/*.xml; do
        [ -e "$XMLFILE" ] || continue
        mv "$XMLFILE" "$XMLFILE.$TIMESTAMP"
        echo "  --> Rotated: $XMLFILE"
    done
fi

echo "[+] Sending HUP signal to ulogd to reload log files..."
pkill -HUP ulogd || echo "  [!] ulogd process not found"

echo "[+] Manual rotation completed."
