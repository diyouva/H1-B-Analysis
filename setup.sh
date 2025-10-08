#!/bin/bash
# SETUP.SH
# Streamlit Cloud environment setup script for:
# "Modeling Post-Study Work Pathways: H-1B, OPT, and CPT under Policy Shock"
# Author: Diyouva C. Novith

echo "=============================================="
echo "Initializing Streamlit Cloud environment..."
echo "=============================================="

# Ensure UTF-8 locale for consistent data parsing
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# Create required directories
mkdir -p data
mkdir -p eda

# Pre-checks
if [ ! -f "data/clean_h1b_data.csv" ]; then
    echo "Note: clean_h1b_data.csv not found in /data"
    echo "You can upload it later or run prepare.py manually inside Streamlit."
else
    echo "Found clean_h1b_data.csv — ready to launch app."
fi

# Optional: print Python version and dependencies for debugging
echo "Python version:"
python --version
echo "Installed packages summary:"
pip list | grep -E "streamlit|plotly|pandas|seaborn|matplotlib|numpy"

echo "=============================================="
echo "Setup completed successfully."
echo "=============================================="