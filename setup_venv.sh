#!/bin/bash
# Banking System TDD - Virtual Environment Setup Script

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Virtual environment setup complete!"
echo "To activate: source venv/bin/activate"
echo "To deactivate: deactivate"