"""Configuration for the Weird AI Experiment Ideator."""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Model Configuration - Using Gemini 2.5 Flash Lite via OpenRouter
# Prefix with openrouter/ to force routing through OpenRouter API
DEFAULT_MODEL = "openrouter/google/gemini-2.5-flash-lite"
GENERATOR_MODEL = os.getenv("GENERATOR_MODEL", DEFAULT_MODEL)
AMPLIFIER_1_MODEL = os.getenv("AMPLIFIER_1_MODEL", DEFAULT_MODEL)  # First weirdness pass
AMPLIFIER_2_MODEL = os.getenv("AMPLIFIER_2_MODEL", DEFAULT_MODEL)  # Second weirdness pass (MAXIMUM CHAOS)
EVALUATOR_MODEL = os.getenv("EVALUATOR_MODEL", DEFAULT_MODEL)
CATEGORIZER_MODEL = os.getenv("CATEGORIZER_MODEL", DEFAULT_MODEL)
SYNTHESIZER_MODEL = os.getenv("SYNTHESIZER_MODEL", DEFAULT_MODEL)

# Generation Parameters
NUM_IDEAS = int(os.getenv("NUM_IDEAS", "50"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.9"))

# Output Configuration
OUTPUT_DIR = "output"
JSON_DIR = "output/json"
PDF_DIR = "output/pdf"
MARKDOWN_DIR = "output/markdown"
