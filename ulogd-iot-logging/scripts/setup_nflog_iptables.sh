#!/bin/bash

# Mô tả: Script tạo các luật iptables gửi log đến các group NFLOG khác nhau
# Tương ứng với các stack trong ulogd.conf.in.user:
# - group 32: LOGEMU (full.log)
# - group 33: LOGEMU (chế độ khác)
# - group 34: JSON log (firewall_log.json)
# - group 100: XML log (ulogd-pkt-sample.xml)

echo "[+] Flushing existing rules..."
iptables -F

echo "[+] Adding NFLOG rules to INPUT chain..."

# Logging all incoming packets to group 32 (text log)
iptables -A INPUT -m limit --limit 2/sec -j NFLOG --nflog-group 32 --nflog-prefix "INPUT_LOGEMU"

# Logging all incoming packets to group 33 (text log variant)
iptables -A INPUT -m limit --limit 2/sec -j NFLOG --nflog-group 33 --nflog-prefix "INPUT_LOGEMU2"

# Logging all incoming packets to group 34 (JSON log)
iptables -A INPUT -m limit --limit 2/sec -j NFLOG --nflog-group 34 --nflog-prefix "INPUT_JSON"

# Logging all incoming packets to group 100 (XML log)
iptables -A INPUT -m limit --limit 2/sec -j NFLOG --nflog-group 100 --nflog-prefix "INPUT_XML"

echo "[+] Done! Current iptables rules:"
iptables -L -n -v
