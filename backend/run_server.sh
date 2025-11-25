#!/bin/bash

# 1. Activate the virtual environment
source venv/bin/activate

# 2. Upgrade pip just in case
pip install --upgrade pip

# 3. Install all the required libraries from the file
echo "Installing dependencies..."
pip install -r requirements.txt

# 4. Run the server
echo "Starting the server..."
python main.py