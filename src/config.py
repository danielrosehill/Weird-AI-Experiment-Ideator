"""Configuration for the Weird AI Experiment Ideator."""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Model - Gemini 2.5 Flash Lite via OpenRouter
DEFAULT_MODEL = "openrouter/google/gemini-2.5-flash-lite"

# Generation Parameters
NUM_IDEAS = int(os.getenv("NUM_IDEAS", "15"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.9"))

# Output paths
OUTPUT_DIR = "output"
JSON_DIR = "output/json"
PDF_DIR = "output/pdf"
MARKDOWN_DIR = "output/markdown"
