#!/bin/bash
set -e

# This script builds the bite-py package and its skale_te dependency,
# placing the resulting wheel files in the final_dist directory.

LIBS_DIR="$(pwd)/libs"
mkdir -p "$LIBS_DIR"

if [ ! -f "$LIBS_DIR/libcrypto.so.1.1" ]; then
    echo "Downloading OpenSSL 1.1.1 libraries..."
    ARCH=$(uname -m)

    if [ "$ARCH" = "x86_64" ]; then
        wget -q "https://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb" -O /tmp/libssl1.1.deb
        dpkg-deb -x /tmp/libssl1.1.deb /tmp/openssl-extract
        cp /tmp/openssl-extract/usr/lib/x86_64-linux-gnu/libcrypto.so.1.1 "$LIBS_DIR/"
        cp /tmp/openssl-extract/usr/lib/x86_64-linux-gnu/libssl.so.1.1 "$LIBS_DIR/"
        rm -rf /tmp/libssl1.1.deb /tmp/openssl-extract
        echo "OpenSSL 1.1.1 libraries installed to $LIBS_DIR"
    else
        echo "Warning: Unsupported architecture $ARCH, skipping OpenSSL download"
    fi
fi

if [ -d "$LIBS_DIR" ]; then
    export LD_LIBRARY_PATH="$LIBS_DIR:$LD_LIBRARY_PATH"
    echo "LD_LIBRARY_PATH configured for OpenSSL 1.1.1"
fi

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt
pip install -q pytest pytest-asyncio build

echo "Running tests..."
pytest tests/ -v

echo "Building bite-py..."
python3 -m build .

echo "Build complete! Files are in 'dist' directory:"
ls -1 dist/
