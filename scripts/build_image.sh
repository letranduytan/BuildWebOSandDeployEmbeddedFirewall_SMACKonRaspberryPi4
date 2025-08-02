#!/bin/bash
set -e

# ===================== CONFIGURATION =====================
DEVICE="raspberrypi4-64"
# Choose master or specific version branch (e.g. 2.19.1 if patch ≥1)
BRANCH="master"
CPU_LOGICAL=$(nproc)
CPU_BUILD=$(( CPU_LOGICAL / 2 ))  # Recommended parallel build (use ~50‑70% of CPUs)
PREMIRROR="http://webosimg.lge.com/downloads"
SSTATEMIRROR="http://webosimg.lge.com/build-artifacts/webos/master/sstate-cache"
# ===========================================================

echo "[1/8] Updating system..."
sudo apt update && sudo apt upgrade -y

echo "[2/8] Installing prerequisites..."
sudo apt install -y build-essential cmake git curl autoconf automake bison flex gawk libtool pkg-config docker.io

echo "[3/8] Configuring Docker..."
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
echo "Please log out and log back in for Docker access."

echo "[4/8] Cloning webOS OSE build repo..."
if [ ! -d "build-webos" ]; then
    git clone https://github.com/webosose/build-webos.git
fi
cd build-webos
git checkout $BRANCH

echo "[5/8] Installing build prerequisites..."
sudo scripts/prerequisites.sh

echo "[6/8] Configuring build using mcf..."
./mcf -p $CPU_BUILD -b $CPU_BUILD \
    --premirror $PREMIRROR \
    --sstatemirror $SSTATEMIRROR \
    $DEVICE

echo "[7/8] Starting bitbake build..."
source oe-init-build-env
bitbake webos-image

echo "[8/8] Build completed. Checking output image..."
IMAGE_DIR="./BUILD/deploy/images/$DEVICE/"
ls -lh $IMAGE_DIR
echo "Your image should be here: $IMAGE_DIR"
