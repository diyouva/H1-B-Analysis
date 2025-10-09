#!/bin/bash
# ==============================================================
# setup.sh — Environment setup for Streamlit Cloud and Local Run
# ==============================================================

echo "----------------------------------------------"
echo "Initializing Streamlit environment..."
echo "----------------------------------------------"

# Locale setup for UTF-8 consistency
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# Create required directories if missing
mkdir -p ~/.streamlit
mkdir -p data
mkdir -p eda

# Generate minimal Streamlit server config if not present
if [ ! -f ~/.streamlit/config.toml ]; then
cat <<EOF > ~/.streamlit/config.toml
[server]
headless = true
enableCORS = false
port = \$PORT
EOF
fi

# Print Python version and top-level packages
echo "Python version: $(python --version)"
echo "Key packages installed:"
pip list | grep -E "streamlit|plotly|pandas|seaborn|matplotlib|numpy" || true

echo "----------------------------------------------"
echo "Environment ready. Launching Streamlit app..."
echo "----------------------------------------------"

# Safe entry point
exec streamlit run app.py