# Test Case: Default Drop Behavior

**Description:** Ensure that invalid or malformed packets are dropped as expected.

**Steps:**
1. Send TCP packet with `FIN+SYN` flags.
2. Send packet with invalid MSS.
3. Send packet from IP in blacklist (e.g., 10.0.0.1).

**Expected Result:** All such packets should be dropped.

**Tools:** hping3, scapy
