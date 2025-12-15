# Weird AI Experiment Ideator

A multi-agent CrewAI system that generates, evaluates, and refines creative AI experiment ideas using **blind multi-pass review architecture**.

## 🎯 Experiment Overview

This project explores whether a multi-agent system with **blinded reviewers** can generate more interesting and creative ideas than a single LLM. Instead of one AI generating ideas, we use a sequential pipeline where each agent builds upon previous work **without knowing what other agents have done**.

### The Core Question
Can independent, blind peer review by AI agents produce more creative and surprising ideas than traditional single-pass generation?

## 🏗️ Architecture: Multi-Pass Blind Review

```
┌─────────────────────────────────────────────────┐
│  STAGE 1: Initial Generation                     │
│  Generator Agent (gemini-2.5-flash-lite)         │
│  ├─ Generates 15 surprising, playful AI ideas    │
│  └─ Temperature: 0.9 (high creativity)           │
└──────────────────┬──────────────────────────────┘
                   │
                   ├─── Ideas passed forward →
                   ▼
┌─────────────────────────────────────────────────┐
│  STAGE 2: Blind Review #1 (Interest & Surprise) │
│  Reviewer Agent 1 (gemini-2.5-flash-lite)        │
│  ├─ Reviews ideas WITHOUT knowing origin         │
│  ├─ Makes each idea MORE interesting             │
│  ├─ Adds depth, unexpected twists                │
│  └─ Temperature: 0.95 (maximum creativity)       │
└──────────────────┬──────────────────────────────┘
                   │
                   ├─── Enhanced ideas →
                   ▼
┌─────────────────────────────────────────────────┐
│  STAGE 3: Blind Review #2 (Shareability)        │
│  Reviewer Agent 2 (gemini-2.5-flash-lite)        │
│  ├─ Reviews WITHOUT knowing prior feedback       │
│  ├─ Finds "viral kernel" in each idea            │
│  ├─ Makes ideas compelling and shareable         │
│  └─ Temperature: 0.9                             │
└──────────────────┬──────────────────────────────┘
                   │
                   ├─── Final versions →
                   ▼
┌─────────────────────────────────────────────────┐
│  STAGE 4: Synthesis & Actionability              │
│  Builder Agent (gemini-2.5-flash-lite)           │
│  ├─ Selects best ideas from refined pool         │
│  ├─ Creates actionable implementation plans      │
│  ├─ Specifies tech stack, MVP approach           │
│  └─ Temperature: 0.7 (balanced)                  │
└──────────────────────────────────────────────────┘
```

### 🎭 Why Blind Review?

Each reviewer agent is explicitly told:
- **"You don't know who created these ideas"**
- **"You don't know if anyone else has reviewed them"**
- **"This is a BLIND REVIEW"**

This prevents agents from:
- Being deferential to the "original creator"
- Assuming someone else has already improved the ideas
- Making minimal changes out of politeness
- Converging on safe, conservative edits

The result: **Each pass genuinely transforms the ideas**, building creative momentum across the pipeline.

## 📊 Experiment Results

**Run Date:** December 16, 2025
**Model Used:** `gemini-2.5-flash-lite` across all agents
**Ideas Generated:** 15 initial concepts → 3 review passes → 10 final actionable projects

### 📥 Download Full Results

**[📄 Download Complete Results (PDF)](output/pdf/20251216_012023.pdf)**

The PDF contains:
- All 15 original ideas from Stage 1
- Enhanced versions from both blind review passes
- Final synthesized ideas with implementation plans
- Complete evolution of each concept through the pipeline

### 🎨 Sample Ideas Generated

The system produced genuinely surprising concepts like:

1. **Algorithmic Dream Weaver** → **Somnium Architect**
   AI that analyzes your day and generates personalized dream narratives designed to prime your subconscious for creative problem-solving

2. **Empathy Synthesizer for Objects** → **Sentient Echoes of the Mundane**
   AI that gives inanimate objects a "shadow history," imagining their existence from raw materials to current state

3. **Lost Language Reconstructor** → **Cryptic Lexicon of Unreality**
   AI that builds entire linguistic ecosystems for fictional civilizations from text fragments

4. **Impossible Playlist Curator**
   Playlists for paradoxical scenarios like "Music for a Penguin Commuting to a Tropical Beach"

5. **Botany of Imagination Gardener**
   AI that "grows" entirely fictional plant species with scientific-sounding descriptions

**Observation:** Each blind review pass added substantial depth, emotional resonance, and actionable detail to the original concepts.

## Features

- **Blind Multi-Pass Review**: Independent agents review without knowledge of prior feedback
- **Cost-Effective**: Uses cheap, creative models from OpenRouter (configurable)
- **Anti-Repetition**: Multi-agent evaluation explicitly identifies and filters similar ideas
- **Progressive Enhancement**: Each pass builds on previous work while maintaining creative independence
- **Flexible Configuration**: Easy to adjust number of ideas, models, temperature, etc.
- **Detailed Output**: Markdown and PDF reports with complete evolution of ideas


## Installation

### Prerequisites

- Python 3.10+
- OpenRouter API key ([get one here](https://openrouter.ai/))

### Setup

1. Clone the repository:
```bash
cd ~/repos/github/Weird-AI-Experiment-Ideator
```

2. Create and activate a virtual environment using `uv`:
```bash
uv venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
uv pip install -e .
```

4. Configure your environment:
```bash
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
```

## Configuration

Edit `.env` to customize the system:

```bash
# Your OpenRouter API key
OPENROUTER_API_KEY=your_key_here

# Model configuration (currently using gemini-2.5-flash-lite across all agents)
DEFAULT_MODEL=google/gemini-2.0-flash-001

# Temperature settings per agent
GENERATOR_TEMP=0.9      # Initial idea generation
REVIEWER_1_TEMP=0.95    # First blind review (maximize creativity)
REVIEWER_2_TEMP=0.9     # Second blind review (shareability focus)
SYNTHESIZER_TEMP=0.7    # Final synthesis (balanced)

# Generation parameters
NUM_IDEAS=15            # Number of ideas to generate
```

### Recommended Cost-Effective Models

The experiment used `gemini-2.5-flash-lite` for all agents, but you can configure different models:

**Fast & Creative (Generator/Reviewers):**
- `google/gemini-2.0-flash-001` - Excellent creativity, very cheap
- `meta-llama/llama-3.1-8b-instruct` - Good creativity, budget-friendly
- `mistralai/mistral-7b-instruct` - Solid balance

**Higher Quality (Synthesizer):**
- `anthropic/claude-3.5-haiku` - Great quality/cost ratio
- `anthropic/claude-3-haiku` - Cheaper alternative
- `openai/gpt-4o-mini` - OpenAI's budget model

## Usage

Run the ideation session:

```bash
python main.py
```

The system will execute the multi-pass pipeline:

1. **Stage 1**: Generate initial ideas with high creativity
2. **Stage 2**: First blind review adds depth and surprise
3. **Stage 3**: Second blind review enhances shareability
4. **Stage 4**: Final synthesis creates actionable plans

Output is saved to:
- `output/markdown/YYYYMMDD_HHMMSS_ideas.md` - Full multi-stage breakdown
- `output/pdf/YYYYMMDD_HHMMSS.pdf` - Complete results as PDF

## Output Structure

Each output contains:

### Stage 1: Initial Generation
- 15 original, playful AI experiment ideas
- Each with a conceptual hook and description

### Stage 2: Blind Review #1 (Interest & Surprise)
- Enhanced versions of all ideas
- Added depth, unexpected twists, emotional resonance
- No knowledge of original creator

### Stage 3: Blind Review #2 (Shareability)
- Further refined versions
- Focus on "viral kernel" and compelling narratives
- Independent of first review

### Stage 4: Synthesis
- Top 10 ideas selected from refined pool
- Complete implementation plans
- Tech stack, MVP approach, deployment strategy

## Cost Estimation

Using `gemini-2.5-flash-lite` for the full pipeline:

- **Per session**: Approximately $0.05 - $0.15 USD
- **Token usage**: ~40K-80K tokens total (varies with idea count)
- **Time**: 3-8 minutes for complete 4-stage pipeline

The blind review architecture adds minimal cost while substantially improving idea quality. Cost scales primarily with `NUM_IDEAS` setting.

## Customization

### Adjusting Temperature Per Stage

Each stage has independent temperature control in `.env`:

```bash
GENERATOR_TEMP=0.9      # Initial ideas (high creativity)
REVIEWER_1_TEMP=0.95    # First review (maximum creativity)
REVIEWER_2_TEMP=0.9     # Second review (balanced)
SYNTHESIZER_TEMP=0.7    # Final plans (focused)
```

**Recommendations:**
- **More wild ideas**: Increase all temperatures to 1.0-1.2
- **More practical focus**: Lower reviewer temps to 0.7-0.8
- **Balanced approach**: Keep generator/reviewers at 0.9, synthesizer at 0.7

### Changing Idea Count

Set `NUM_IDEAS` in `.env`:
- **10-15 ideas**: Faster, focused sessions (~5 mins)
- **20-30 ideas**: Broader exploration (~10 mins)
- **50+ ideas**: Maximum diversity, longer runtime

### Customizing Agent Prompts

Edit agent backstories in [src/agents.py](src/agents.py:1) to change focus:

**Example:** Make ideas more technical:
```python
backstory="""You design experiments focused on technical depth and
engineering feasibility. You love ideas that showcase interesting
algorithms, novel architectures, or clever technical solutions..."""
```

## Troubleshooting

### API Key Issues
```
❌ Error: OPENROUTER_API_KEY not found
```
Solution: Ensure `.env` file exists and contains your API key.

### Rate Limiting
If you hit rate limits, you can:
- Use slower, cheaper models
- Add delays between agent tasks
- Reduce `NUM_IDEAS`

### Ideas Feel Too Similar
If ideas lack diversity:
- Increase `GENERATOR_TEMP` and `REVIEWER_1_TEMP` to 1.0+
- Try different models (gemini-flash tends toward high creativity)
- Check agent backstories - ensure they emphasize variety
- The blind review architecture should naturally combat repetition

## Development

Project structure:
```
.
├── main.py              # Entry point
├── src/
│   ├── agents.py        # Agent definitions (4 specialized agents)
│   ├── tasks.py         # Task definitions (generation, reviews, synthesis)
│   ├── crew.py          # Crew orchestration (sequential pipeline)
│   └── config.py        # Configuration
├── output/
│   ├── markdown/        # Full multi-stage results
│   └── pdf/             # PDF versions
├── pyproject.toml       # Dependencies
└── README.md
```

### Key Implementation Details

The blind review mechanism is enforced in [src/agents.py](src/agents.py:47):

```python
def create_reviewer_agent_1() -> Agent:
    return Agent(
        role="Independent Idea Reviewer",
        backstory="""You've been asked to do a BLIND REVIEW of some AI experiment ideas.
        You don't know who created them or if anyone else has reviewed them.

        Your job is simple: take each idea and find the MORE INTERESTING version hiding inside...
        """
    )
```

Each reviewer genuinely believes it's the first/only reviewer, creating independent creative enhancement.

## Contributing

This is a research experiment exploring multi-agent creative workflows. Ideas for improvements:
- Different blinding strategies
- More review passes
- Quantitative evaluation metrics for creativity
- Alternative pipeline architectures

## License

MIT License - see LICENSE file for details.

## Credits

- Built with [CrewAI](https://github.com/joaomdmoura/crewAI)
- Uses [OpenRouter](https://openrouter.ai/) for LLM access
- Created by Daniel Rosehill

## Related Projects

- [System Prompt](system-prompt.md) - The original system prompt that inspired this project
- [Daniel's GitHub](https://github.com/danielrosehill) - More AI experiments and tools
