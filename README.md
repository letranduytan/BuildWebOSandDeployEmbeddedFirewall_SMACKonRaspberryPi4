# Build WebOS and deploy embedded firewall SMACK on Raspberry Pi 4
<p align="center">
<a href="https://fb.com/duytan.hh" target="_blank"><img src="https://img.shields.io/badge/Facebook%20-%20%230866FF"></a>
<a href="https://t.me/duytan2003" target="_blank"><img src="https://img.shields.io/badge/Telegram%20-%20%2333CCFF"></a>
<a href="https://www.linkedin.com/in/l%C3%AA-tr%E1%BA%A7n-duy-t%C3%A2n-81112a23a/" target="_blank"><img src="https://img.shields.io/badge/Linkedin%20-%20%2300CCFF"></a>
</p>

## Overview

This project is developed based on publicly shared resources from **LG Electronics R&D Vietnam – Da Nang branch**, serving training and research activities at the **LG Lab**.

It focuses on building a **custom WebOS** embedded on **Raspberry Pi 4**, integrating key Linux security features to enhance embedded system security — especially for **automotive** and **edge devices**.

## Key Features

- 🔧 **Customized WebOS Build**  
  Modular OS build system tailored for Raspberry Pi 4.

- 🔐 **Security Integration**
  - **Firewall**: Configured using `nftables` to filter traffic, detect threats, and prevent unauthorized access.
  - **SMACK (Simplified Mandatory Access Control Kernel)**: Enforces mandatory access control at the kernel level.

## Objectives

- Strengthen the security of embedded Linux-based systems
- Provide a hands-on learning platform for security in automotive and IoT environments
- Demonstrate practical integration of open-source Linux security features

## Applications

This system is suitable for:
- Automotive control units (ECUs)
- Edge computing devices
- Secure gateways in IoT environments

---
# Build webOS OSE on Raspberry Pi 4

### Related Documentation

* [Building webOS OSE Guide](https://www.webosose.org/docs/guides/setup/building-webos-ose/)
* [Flashing webOS OSE Guide](https://www.webosose.org/docs/guides/setup/flashing-webos-ose/)

## I. PREREQUISITES

### 1. Required Knowledge

* Basic networking concepts
* Linux command line
* Understanding of kernel modules, SMACK

### 2. Hardware

* Raspberry Pi 4 (8GB RAM recommended)
* SD card flashed with webOS OSE

### 3. Software Tools

```bash
sudo apt install build-essential cmake git curl autoconf automake bison flex gawk libtool pkg-config docker.io git-all
```

### 4. Initial Setup

* Ensure SSH access to Raspberry Pi

---

## II. CONFIGURATIONS

### 1. Build Environment

#### Step 1: Update system and install dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install build-essential cmake git curl
sudo apt install autoconf automake bison flex gawk libtool pkg-config
sudo apt install git-all docker.io
sudo systemctl enable docker && sudo systemctl start docker
sudo usermod -aG docker $USER
```

#### Step 2: Clone & configure build system

```bash
git clone https://github.com/webosose/build-webos.git
cd build-webos
git checkout 2.20
sudo scripts/prerequisites.sh
./mcf -p 3 -b 3 raspberrypi4-64
```

#### Step 3: Kernel and Security Configurations

Modify the following files to enable SMACK and necessary kernel modules:

**File 1: `meta-webosose/meta-webos-raspberrypi/recipes-kernel/linux/linux-raspberrypi/bridge.cfg`**

```plaintext
CONFIG_NETFILTER_XT_MATCH_CONNBYTES=y
CONFIG_NETFILTER_XT_MATCH_CONNLIMIT=y
CONFIG_NETFILTER_XT_MATCH_IPRANGE=y
CONFIG_NETFILTER_XT_MATCH_LENGTH=y
CONFIG_NETFILTER_XT_MATCH_LIMIT=y
CONFIG_NETFILTER_XT_MATCH_MAC=y
CONFIG_NETFILTER_XT_MATCH_QUOTA=y
CONFIG_NETFILTER_XT_TARGET_NFLOG=y
CONFIG_NF_LOG_IPV4=y
CONFIG_NETFILTER_XT_MATCH_RECENT=y
CONFIG_NETFILTER_XT_MATCH_TCPMSS=y
CONFIG_NETFILTER_XT_TARGET_TCPMSS=y
CONFIG_NETFILTER_XT_MATCH_HASHLIMIT=y
CONFIG_NETFILTER_XT_MATCH_NFACCT=y
CONFIG_IP_SET=y
CONFIG_IP_SET_HASH_IP=y
CONFIG_IP_SET_HASH_NET=y
CONFIG_NETFILTER_XT_SET=y
```

**File 2: `meta-webosose/meta-webos-raspberrypi/recipes-kernel/linux/linux-raspberrypi/security.cfg`**

```plaintext
CONFIG_SECURITY_SMACK=y
CONFIG_DEFAULT_SECURITY="smack"
CONFIG_DEFAULT_SECURITY_SMACK=y
CONFIG_TMPFS_XATTR=y
CONFIG_SECURITY_SMACK_BRINGUP=y
CONFIG_LSM="lockdown,yama,loadpin,safesetid,integrity,smack,selinux,tomoyo,apparmor"
CONFIG_IKCONFIG_PROC=y
CONFIG_IKCONFIG=y
CONFIG_PROC_FS=y
CONFIG_EXPERT=y
```

**File 3: `meta-webosose/meta-webos/recipes-core/images/webos-image.bb`**
Append:

```plaintext
WEBOS_IMAGE_EXTRA_INSTALL:append = " htop tcpdump ipset apt kernel-module-xt-hashlimit "
```

**File 4: `conf/local.conf`**
Append:

```plaintext
DISTRO_FEATURES:append = " smack"
DISTRO_FEATURES:append = " smack-bringup"
```

#### Step 4: Build image

```bash
source oe-init-build-env
bitbake webos-image
```

#### Step 5: Extract image and flash SD card

```bash
cd BUILD/deploy/images/raspberrypi4-64
bunzip2 webos-image-raspberrypi4-64.rootfs.wic.bz2
lsblk
sudo umount /dev/sdX1
sudo dd bs=4M if=webos-image-raspberrypi4-64.rootfs.wic of=/dev/sdX status=progress
sudo umount /dev/sdX
```

---

## III. PROBLEMS & SOLUTIONS

### 1. Qtbase build error (RAM limitation)

```bash
sudo fallocate -l 20G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 2. aktualizr do\_fetch failure

* Update `GARAGE_SIGN_PV` variable
* Replace old checksum lines in `SRC_URI[]`

---

## IV. TESTING

Once image is flashed and running on Raspberry Pi:

* Check SMACK policies using: `cat /proc/self/attr/current`
* Verify included utilities: `htop`, `tcpdump`, etc.
* Confirm SMACK kernel support using: `dmesg | grep smack`

---

## V. APPENDIX

Useful commands:

* `bitbake -c cleanall webos-image` — clean build
* `docker ps`, `docker system prune` — manage build containers
* `oe-init-build-env` — reenter build environment


