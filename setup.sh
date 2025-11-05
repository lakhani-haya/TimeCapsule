#!/bin/bash

echo "Setting up AI Time Capsule... "
echo ""

# Check if Python is ins
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "Python found!"

# Create virtual environment
echo "Creating virtual environment..."
python -m venv time_capsule_env

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source time_capsule_env/Scripts/activate
else
    source time_capsule_env/bin/activate
fi

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Setup complete! 🎉"
echo ""
echo "To run the app:"
echo "1. Activate the environment:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "   time_capsule_env\\Scripts\\activate"
else
    echo "   source time_capsule_env/bin/activate"
fi
echo "2. Run the app:"
echo "   streamlit run app.py"
echo ""
echo "💌 Happy letter writing! ✨"
