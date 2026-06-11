#!/bin/bash
# Build bite.py for Ubuntu 22.04 using Docker

set -e

echo "Building bite-py for Ubuntu 22.04..."

# Create a temporary Dockerfile
cat > Dockerfile.ubuntu22 << 'EOF'
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    build-essential \
    libffi-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY . .

# Use Ubuntu 22 specific requirements without t-encrypt
RUN python3 -m venv venv
RUN . ./venv/bin/activate && pip install --upgrade pip
RUN . ./venv/bin/activate && pip install -r requirements-ubuntu22-base.txt
RUN . ./venv/bin/activate && pip install build wheel

# Install real t_encrypt package from archive
RUN mkdir -p /tmp/t_encrypt_install && \
    cd /tmp/t_encrypt_install && \
    tar -xf /workspace/libt_encrypt_python.tar.xz && \
    mkdir -p t_encrypt_package/t_encrypt && \
    cp libt_encrypt_python.so t_encrypt_package/t_encrypt/libencrypt.so && \
    cp /workspace/libs/libcrypto.so.1.1 /workspace/libs/libssl.so.1.1 t_encrypt_package/t_encrypt/ && \
    cp /workspace/t_encrypt_package/t_encrypt/__init__.py t_encrypt_package/t_encrypt/ && \
    cp /workspace/t_encrypt_package/setup.py t_encrypt_package/ && \
    cd t_encrypt_package && . /workspace/venv/bin/activate && pip install .

# Create OpenSSL libs directory
RUN mkdir -p libs && \
    wget -q "https://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb" -O /tmp/libssl1.1.deb && \
    dpkg-deb -x /tmp/libssl1.1.deb /tmp/openssl-extract && \
    cp /tmp/openssl-extract/usr/lib/x86_64-linux-gnu/libcrypto.so.1.1 libs/ && \
    cp /tmp/openssl-extract/usr/lib/x86_64-linux-gnu/libssl.so.1.1 libs/ && \
    rm -rf /tmp/libssl1.1.deb /tmp/openssl-extract

# Build the package
RUN export LD_LIBRARY_PATH="$(pwd)/libs:$LD_LIBRARY_PATH" && \
    . ./venv/bin/activate && python -m build .

# Also build the t_encrypt wheel
RUN cd /tmp/t_encrypt_install/t_encrypt_package && \
    . /workspace/venv/bin/activate && python -m build . && \
    cp dist/*.whl /workspace/dist/

CMD ["cp", "-r", "dist/", "/output/"]
EOF

# Build the Docker image
echo "Building Docker image..."
docker build -f Dockerfile.ubuntu22 -t bite-py-ubuntu22 .

# Create output directory
mkdir -p dist-ubuntu22

# Run the container and copy artifacts
echo "Running build in Ubuntu 22.04 container..."
docker run --rm -v "$(pwd)/dist-ubuntu22:/output" bite-py-ubuntu22 sh -c "cp -r dist/* /output/"

# Clean up
rm Dockerfile.ubuntu22

echo "Build complete! Artifacts are in dist-ubuntu22/"
ls -la dist-ubuntu22/
