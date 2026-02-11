#!/bin/bash
# Find where the app is located
DIR=$(dirname "$0")

cd "$DIR"

export PATH="$DIR/../Resources/python_env/bin:$PATH"
export PYTHONPATH="$DIR/../Resources/python_env/lib/python3.11/site-packages"

# Launch your Nuitka binary
exec "$DIR/gui.bin"