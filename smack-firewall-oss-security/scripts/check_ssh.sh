#!/bin/sh
echo "=== Checking Dropbear SSH root login policy ==="

dropbear_status=$(ps | grep '[d]ropbear' | grep -E -- '-w|-g')

if [ -z "$dropbear_status" ]; then
    echo "[OK] Dropbear allows root login"
else
    echo "[WARN] Dropbear is running with root login restrictions: $dropbear_status"
fi
