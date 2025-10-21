#!/usr/bin/env bash
set -o errexit

echo "🛠 Using Python version:"
python --version

# Upgrade pip and build tools (optional but safer)
pip install --upgrade pip setuptools wheel

# 🚫 Skip building from source — only use prebuilt wheels
pip install --only-binary=:all: -r requirements.txt

