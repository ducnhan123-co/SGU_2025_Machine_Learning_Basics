#!/bin/bash

# Setup script for Titanic ML Project

echo "🚀 Setting up Titanic ML Project..."
echo ""

# Check Python version
echo "📌 Checking Python version..."
python --version

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "✅ Virtual environment created"
else
    echo "⚠️  Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo ""
echo "📥 Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "📁 Creating directories..."
mkdir -p scripts
mkdir -p process/exps
mkdir -p logs

# Make scripts executable
echo ""
echo "⚙️  Making scripts executable..."
chmod +x scripts/create_new_experiment.py

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "📝 Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Read documentation: cat START_HERE.md"
echo "3. Create new experiment: python scripts/create_new_experiment.py"
echo ""
echo "📚 Documentation files:"
echo "- START_HERE.md - Get started here"
echo "- QUICK_START.md - Quick guide"
echo "- WORKFLOW_GUIDE.md - Complete workflow"
echo ""
