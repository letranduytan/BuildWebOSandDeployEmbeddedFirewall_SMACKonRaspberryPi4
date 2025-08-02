# IPv4/IPv6 Network Test Scripts

This module provides senders and receivers for testing various packet types (unicast, broadcast, multicast) over IPv4 and IPv6.

## Structure

- `send/`: Scripts that send packets to specific IP types.
- `recv/`: Scripts that listen and print packets received from specific IP types.
- `common/utils.py`: Common socket helpers.

## Usage Example

### Send IPv4 broadcast
```bash
python3 ipv4/send/broadcast_sender.py
