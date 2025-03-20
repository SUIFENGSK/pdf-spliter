#!/bin/bash

# Set default DPI value
DEFAULT_DPI=300

# Use provided DPI or default if not provided
DPI=${1:-$DEFAULT_DPI}

# Delete old files in output folder
rm -rf output_images

# Activate the virtual environment
source .venv/bin/activate

# Run the script with the specified or default DPI
python main.py --dpi $DPI