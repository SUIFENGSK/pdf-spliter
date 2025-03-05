#!/bin/bash

# Delete old files in output folder
rm -rf output_images

# Activate the virtual environment
source .venv/bin/activate

# Run the script
python main.py