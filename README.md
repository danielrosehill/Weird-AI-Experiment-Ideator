# Weird AI Experiment Ideator

A multi-agent CrewAI system that generates, evaluates, categorizes, and synthesizes creative AI experiment ideas.

## Overview

This project uses a sophisticated multi-agent workflow to overcome the common challenge of repetitive idea generation. Instead of a single LLM generating ideas, we employ a crew of four specialized agents:

1. **Generator Agent**: Creates 50 diverse, creative AI experiment ideas spanning multiple domains
2. **Evaluator Agent**: Critically assesses each idea for creativity, feasibility, uniqueness, and impact
3. **Categorizer Agent**: Organizes ideas into thematic categories and identifies patterns
4. **Synthesizer Agent**: Creates a comprehensive report with insights and recommendations

## Features

- **Cost-Effective**: Uses cheap, creative models from OpenRouter (configurable)
- **Anti-Repetition**: Multi-agent evaluation explicitly identifies and filters similar ideas
- **Comprehensive Analysis**: Not just ideas, but evaluation scores, categories, and actionable insights
- **Flexible Configuration**: Easy to adjust number of ideas, models, temperature, etc.
- **Detailed Output**: Markdown reports with executive summaries, top ideas, feasibility tiers, and commercial opportunities

## Architecture

```
┌─────────────────────┐
│  Generator Agent    │  Creates 50 diverse ideas
│  (High creativity)  │  (meta-llama/llama-3.1-8b)
└──────────┬──────────┘
           │
           ├─────────────────────┐
           │                     │
           ▼                     ▼
┌─────────────────────┐ ┌─────────────────────┐
│  Evaluator Agent    │ │ Categorizer Agent   │
│  (Critical analysis)│ │ (Pattern finding)   │
└──────────┬──────────┘ └──────────┬──────────┘
           │                       │
           └───────────┬───────────┘
                       ▼
           ┌─────────────────────┐
           │ Synthesizer Agent   │
           │ (Report generation) │
           │ (claude-3.5-haiku)  │
           └─────────────────────┘
```

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

# Models (choose from OpenRouter's catalog)
GENERATOR_MODEL=meta-llama/llama-3.1-8b-instruct
EVALUATOR_MODEL=meta-llama/llama-3.1-8b-instruct
CATEGORIZER_MODEL=meta-llama/llama-3.1-8b-instruct
SYNTHESIZER_MODEL=anthropic/claude-3.5-haiku

# Generation parameters
NUM_IDEAS=50          # Number of ideas to generate
TEMPERATURE=0.9       # Higher = more creative/random
```

### Recommended Cost-Effective Models

For the generator, evaluator, and categorizer agents, consider these cheap, creative options:

- `meta-llama/llama-3.1-8b-instruct` - Very cheap, good creativity
- `google/gemini-flash-1.5-8b` - Fast and cheap
- `mistralai/mistral-7b-instruct` - Good balance
- `nousresearch/hermes-3-llama-3.1-405b` - Higher quality, still cheap

For the synthesizer (report writing), you might want higher quality:

- `anthropic/claude-3.5-haiku` - Great quality/cost ratio
- `anthropic/claude-3-haiku` - Cheaper alternative
- `openai/gpt-4o-mini` - OpenAI's budget model

## Usage

Run the ideation session:

```bash
python main.py
```

The system will:
1. Generate 50 diverse AI experiment ideas
2. Evaluate each idea across multiple criteria
3. Categorize ideas into thematic groups
4. Produce a comprehensive synthesis report

Output is saved to `output/ideation_report_YYYYMMDD_HHMMSS.md`

## Output Structure

The final report includes:

- **Executive Summary**: Overview and key statistics
- **Top Ideas Showcase**: Detailed presentation of the 10-15 best ideas
- **Thematic Analysis**: Categories, patterns, and connections
- **Diversity Assessment**: How well repetition was avoided
- **Feasibility Tiers**: Quick wins, medium-term projects, long-term visions
- **Commercial Opportunities**: Market potential and business models
- **Recommendations**: Prioritization and next steps

## Example Ideas (From Previous Runs)

The system has generated ideas across domains like:
- Multi-agent simulations (geopolitical summits, tech conferences)
- AI in physical spaces (interactive museums, smart cities)
- Social experiments (AI mediators, cultural exchange bots)
- Artistic applications (generative music performances, AI art critics)
- Educational tools (personalized tutors, debate training)
- Unusual interfaces (smell-based AI, haptic storytelling)

## Cost Estimation

Using the recommended models (Llama 3.1 8B for generation/eval/categorization, Claude Haiku for synthesis):

- **Per session**: Approximately $0.10 - $0.50 USD
- **Token usage**: ~50K-150K tokens total
- **Time**: 5-15 minutes depending on models and idea count

You can run many sessions for very little cost, making this ideal for iterative ideation.

## Customization

### Adjusting Creativity vs. Quality

- **More creativity**: Increase `TEMPERATURE` (try 1.0-1.2) and use smaller models
- **Higher quality**: Lower `TEMPERATURE` (try 0.7-0.8) and use larger models like Claude or GPT-4o

### Changing Idea Count

Set `NUM_IDEAS` in `.env`. Note:
- Fewer ideas (20-30): Faster, cheaper, less diversity
- More ideas (50-100): Better diversity, longer runtime, higher cost

### Adding Custom Domains

Edit `src/tasks.py` in the generation task description to emphasize specific domains:

```python
description=f"""Generate {NUM_IDEAS} unique AI experiment ideas.

Focus especially on: robotics, embodied AI, and physical installations.
...
"""
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

### Poor Diversity
If ideas are too similar:
- Increase `TEMPERATURE`
- Try different generator models
- Run multiple smaller sessions instead of one large one

## Development

Project structure:
```
.
├── main.py              # Entry point
├── src/
│   ├── agents.py        # Agent definitions
│   ├── tasks.py         # Task definitions
│   ├── crew.py          # Crew orchestration
│   └── config.py        # Configuration
├── output/              # Generated reports
├── pyproject.toml       # Dependencies
└── README.md
```

## Contributing

This is a personal project, but ideas and improvements are welcome! The system is designed to be easily extensible.

## License

MIT License - see LICENSE file for details.

## Credits

- Built with [CrewAI](https://github.com/joaomdmoura/crewAI)
- Uses [OpenRouter](https://openrouter.ai/) for LLM access
- Created by Daniel Rosehill

## Related Projects

- [System Prompt](system-prompt.md) - The original system prompt that inspired this project
- [Daniel's GitHub](https://github.com/danielrosehill) - More AI experiments and tools
