# ULOGD IoT Logging Stack

This project demonstrates how to use **ULOGD v2** (Netfilter Userspace Logging Daemon) to capture, filter, and log network traffic from firewalls (iptables/NFLOG) into various formats such as plain text, JSON, and XML — optimized for **IoT devices** like Raspberry Pi.

---

## 🔧 Features

- 🔌 Capture packets and flows using **NFLOG** and **NFCT**
- 🧱 Stack-based plugin system: Input → Filter → Output
- 🧾 Log formats supported:
  - Plain Text (LOGEMU)
  - Structured JSON (suitable for ELK stack / MQTT)
  - XML (optional for special systems)
- 📈 Kibana Dashboard for visualization
- 🔄 Manual and automated log rotation (via `logrotate` or scripts)

---