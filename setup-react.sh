#!/bin/bash
# React Frontend Setup Script for Linux/Mac

echo ""
echo "========================================"
echo "AI Memory Tree Chat - React Frontend Setup"
echo "========================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed!"
    echo "Please download and install Node.js from https://nodejs.org/"
    exit 1
fi

echo "✓ Node.js found: "
node --version

echo ""
echo "Installing npm dependencies..."
echo ""

cd frontend-react
npm install

if [ $? -ne 0 ]; then
    echo "ERROR: npm install failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Make sure backend is running: python -m uvicorn backend.main:app --reload"
echo "2. Run: npm run dev"
echo "3. Open browser: http://localhost:3000"
echo ""
