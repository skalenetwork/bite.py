#!/bin/bash
# Installation script for bite.py Ubuntu 22 build

set -e

DIST_DIR="${1:-dist-ubuntu22}"

if [ ! -d "$DIST_DIR" ]; then
    echo "Error: Distribution directory '$DIST_DIR' not found"
    echo "Usage: $0 [dist-directory]"
    exit 1
fi

echo "Installing bite.py Ubuntu 22 compatible packages from $DIST_DIR..."

# Install t_encrypt first (dependency)
T_ENCRYPT_WHEEL=$(find "$DIST_DIR" -name "t_encrypt-*.whl" | head -1)
if [ -n "$T_ENCRYPT_WHEEL" ]; then
    echo "Installing t_encrypt: $T_ENCRYPT_WHEEL"
    pip install "$T_ENCRYPT_WHEEL"
else
    echo "Warning: t_encrypt wheel not found, you may need to install it separately"
fi

# Install bite_py
BITE_WHEEL=$(find "$DIST_DIR" -name "bite_py-*ubuntu22*.whl" | head -1)
if [ -n "$BITE_WHEEL" ]; then
    echo "Installing bite_py: $BITE_WHEEL"
    pip install "$BITE_WHEEL"
else
    echo "Error: bite_py Ubuntu 22 wheel not found in $DIST_DIR"
    exit 1
fi

echo "Installation complete!"
echo ""
echo "To test the installation:"
echo "  python -c \"import bite; print('bite.py installed successfully')\""
echo "  python -c \"import t_encrypt; print('t_encrypt installed successfully')\""