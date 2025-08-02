#!/bin/bash
set -e

# flash_image.sh – Flash a webOS OSE image to microSD card (Linux/macOS)

function usage() {
  echo "Usage: $0 -i <image.wic> -d </dev/sdX or /dev/diskN>"
  echo "Example: $0 -i webos-image-raspberrypi4-64.rootfs.wic -d /dev/sdb"
  exit 1
}

IMAGE=""
DEVICE=""

while getopts "i:d:" opt; do
  case "$opt" in
    i) IMAGE="$OPTARG" ;;
    d) DEVICE="$OPTARG" ;;
    *) usage ;;
  esac
done

if [ -z "$IMAGE" ] || [ -z "$DEVICE" ]; then
  usage
fi

echo "[1] Verifying image file exists..."
if [ ! -f "$IMAGE" ]; then
  echo "Error: image file '$IMAGE' not found."
  exit 1
fi

echo "[2] Unmounting target partitions..."
sudo umount "${DEVICE}"* || true

echo "[3] Flashing image..."
sudo dd bs=4M if="$IMAGE" of="$DEVICE" status=progress conv=fsync

echo "[4] Syncing and unmounting..."
sudo sync
sudo umount "${DEVICE}"* || true

echo "Flash completed successfully to $DEVICE"
echo "Please eject the microSD card and insert it into your target device."
