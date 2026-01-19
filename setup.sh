#!/bin/bash

# Fantasy Football RAG System Setup Script

echo "=================================="
echo "Fantasy Football RAG System Setup"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠ Please edit .env file with your credentials"
else
    echo "✓ .env file already exists"
fi

# Check if Docker is installed
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo ""
    echo "Docker detected. Would you like to start the PostgreSQL database with Docker? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Starting PostgreSQL with pgvector..."
        docker-compose up -d
        echo "✓ Database started"
        echo "Waiting for database to be ready..."
        sleep 5
        
        # Initialize database
        echo "Initializing database..."
        python3 database.py
        echo "✓ Database initialized"
    fi
else
    echo ""
    echo "⚠ Docker not found. Please set up PostgreSQL with pgvector manually."
    echo "  Installation instructions: https://github.com/pgvector/pgvector"
fi

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your OpenAI API key and database credentials"
echo "2. If not using Docker, set up PostgreSQL with pgvector extension"
echo "3. Run 'python database.py' to initialize the database (if not done automatically)"
echo "4. Run 'python example.py' to see the system in action"
echo "5. Use 'python cli.py --help' for command-line interface options"
echo ""
