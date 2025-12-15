#!/bin/bash

# Weird AI Experiment Ideator - Quick Run Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🤖 Weird AI Experiment Ideator"
echo "================================"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${RED}❌ Virtual environment not found${NC}"
    echo "Please run setup first:"
    echo "  uv venv"
    echo "  source .venv/bin/activate"
    echo "  uv pip install -e ."
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found${NC}"
    echo "Please copy .env.example to .env and configure:"
    echo "  cp .env.example .env"
    echo "  # Then edit .env and add your OPENROUTER_API_KEY"
    exit 1
fi

# Source .env
source .env

# Check if API key is set
if [ -z "$OPENROUTER_API_KEY" ] || [ "$OPENROUTER_API_KEY" == "your_api_key_here" ]; then
    echo -e "${RED}❌ OPENROUTER_API_KEY not configured${NC}"
    echo "Please edit .env and add your OpenRouter API key"
    exit 1
fi

echo -e "${GREEN}✓ Environment configured${NC}"
echo ""
echo "Configuration:"
echo "  NUM_IDEAS: ${NUM_IDEAS:-15}"
echo "  MODEL: google/gemini-2.5-flash-lite (via OpenRouter)"
echo "  TEMPERATURE: ${TEMPERATURE:-0.9}"
echo ""

# Activate virtual environment and run
source .venv/bin/activate

# Run the ideation session
echo -e "${YELLOW}🚀 Starting ideation session...${NC}"
echo ""

python main.py

echo ""
echo -e "${GREEN}✅ Done!${NC}"
echo ""
echo "Check the output/ directory for your report."
