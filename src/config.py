"""Configuration for the Weird AI Experiment Ideator."""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Model Configuration
GENERATOR_MODEL = os.getenv("GENERATOR_MODEL", "meta-llama/llama-3.1-8b-instruct")
EVALUATOR_MODEL = os.getenv("EVALUATOR_MODEL", "meta-llama/llama-3.1-8b-instruct")
CATEGORIZER_MODEL = os.getenv("CATEGORIZER_MODEL", "meta-llama/llama-3.1-8b-instruct")
SYNTHESIZER_MODEL = os.getenv("SYNTHESIZER_MODEL", "anthropic/claude-3.5-haiku")

# Generation Parameters
NUM_IDEAS = int(os.getenv("NUM_IDEAS", "50"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.9"))

# Output Configuration
OUTPUT_DIR = "output"
