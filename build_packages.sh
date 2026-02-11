#!/bin/bash
set -e

# Створюємо папку для фінальних артефактів
mkdir -p final_dist

echo "Installing build tool..."
pip install build

echo "Building skale_te dependency..."
python3 -m build local_dependencies/skale_te_pkg
cp local_dependencies/skale_te_pkg/dist/*.whl final_dist/

echo "Building bite-py..."
python3 -m build .
cp dist/*.whl final_dist/

echo "Build complete! Files are in 'final_dist' directory:"
ls -1 final_dist/
