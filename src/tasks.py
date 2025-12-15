"""Task definitions for the Weird AI Experiment Ideator."""
from crewai import Task
from .config import NUM_IDEAS


def create_generation_task(agent) -> Task:
    """Create the initial idea generation task."""
    return Task(
        description=f"""Generate {NUM_IDEAS} interesting, surprising AI experiment ideas.

AVOID:
- Chatbots, assistants, recommendation engines
- Dark, dystopian, horror themes
- Generic "AI for X" applications
- Abstract conceptual art that can't actually be built

LOOK FOR:
- Surprising combinations that make people think
- Playful experiments that reveal something interesting
- Ideas that ask good questions about AI or human behavior
- Things that could actually be built and would be fun to experience

For each idea:
1. **Title** - memorable, intriguing
2. **The Idea** - what is it, what happens (2-3 paragraphs)
3. **The Hook** - why would someone want to try this or share it?

Number them 1 through {NUM_IDEAS}. Keep them DISTINCT and INTERESTING.""",
        agent=agent,
        expected_output=f"A numbered list of {NUM_IDEAS} interesting AI experiment ideas.",
    )


def create_review_task_1(agent, context) -> Task:
    """First blind review - focus on making ideas more interesting/surprising."""
    return Task(
        description="""You're doing an INDEPENDENT BLIND REVIEW of AI experiment ideas.
No one else has reviewed these yet. You're seeing them fresh.

YOUR FOCUS: Make each idea MORE INTERESTING and SURPRISING.

For each idea, ask yourself (but don't explain your reasoning):
- What unexpected twist would make this more memorable?
- What connection to another domain would create surprise?
- What would make someone actually want to try this?

For each idea, output ONLY:
## [Number]. [Title - maybe new, maybe same]
[Your improved version - 2-3 paragraphs describing the idea]

NO explanations. NO "what makes this better". Just the improved idea itself.
Keep things grounded and achievable.""",
        agent=agent,
        context=context,
        expected_output="Improved versions of all ideas - just the ideas, no commentary.",
    )


def create_review_task_2(agent, context) -> Task:
    """Second blind review - focus on shareability and buildability."""
    return Task(
        description="""You're doing an INDEPENDENT BLIND REVIEW of AI experiment ideas.
No one else has reviewed these yet. You're seeing them fresh.

YOUR FOCUS: Find the version that would actually get BUILT and SHARED.

For each idea, output ONLY:
## [Number]. [Title]
[The most compelling, buildable version - 2-3 paragraphs]
**Hook:** [One punchy line that sells it]

NO explanations. NO analysis. Just the idea and its hook.""",
        agent=agent,
        context=context,
        expected_output="The most compelling version of each idea - just ideas and hooks, no commentary.",
    )


def create_synthesis_task(agent, context) -> Task:
    """Final task - pick the best and make them buildable."""
    return Task(
        description="""From all the ideas, pick the 10 BEST and make them REAL.

For each of your TOP 10:

## [Number]. [Title]

**What It Is:** One clear paragraph anyone could understand.

**How to Build It:**
- Tech stack / tools
- MVP version (simplest thing that works)
- Rough cost/effort estimate
- Where it lives (app, website, installation, event, etc.)

**Why It's Great:** The one thing that makes this worth building.

Pick ideas that are INTERESTING + ACHIEVABLE. Keep the magic.""",
        agent=agent,
        context=context,
        expected_output="10 buildable ideas with clear implementation plans.",
    )
