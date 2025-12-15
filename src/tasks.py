"""Task definitions for the Weird AI Experiment Ideator."""
from crewai import Task
from .config import NUM_IDEAS


def create_generation_task(agent) -> Task:
    """Create the idea generation task."""
    return Task(
        description=f"""Generate {NUM_IDEAS} WEIRD, UNCONVENTIONAL AI experiment ideas.

IMPORTANT: DO NOT generate boring, predictable ideas like:
- Chatbots for customer service
- AI for productivity/scheduling
- Personalized recommendations
- Healthcare diagnostics
- Educational tutors
These are BANNED. If you catch yourself writing something like this, DELETE IT.

Each idea MUST be:
- WEIRD - something that makes people do a double-take
- UNEXPECTED - not the obvious application of AI
- MEMORABLE - something people would share and talk about
- EXPERIMENTAL - pushing boundaries of what's "normal"

Draw from domains like:
- Absurdist art installations
- Social experiments that reveal human nature
- AI that intentionally fails in interesting ways
- Posthuman and speculative futures
- Glitch aesthetics and embracing errors
- AI as performance art or ritual
- Systems that are deliberately inefficient but beautiful
- AI that generates meaning from nonsense
- Experiments at the edge of creepy/fascinating
- AI that explores liminal spaces, dreams, boredom

For each idea, provide:
1. **Title**: A memorable, evocative name (not corporate-speak!)
2. **The Weird Concept**: What makes this strange and compelling
3. **How It Works**: Technical approach (but keep it grounded enough to actually do)
4. **Why It Matters**: The deeper insight or question this explores
5. **Vibe Check**: What emotional/aesthetic response does this evoke?

Number each idea clearly (1-{NUM_IDEAS}) and make them DISTINCT.""",
        agent=agent,
        expected_output=f"A list of {NUM_IDEAS} genuinely weird and unconventional AI experiment ideas that push creative boundaries.",
    )


def create_amplification_task_1(agent, context) -> Task:
    """Create the first weirdness amplification task (blinded)."""
    return Task(
        description="""You've been given a collection of INITIAL CONCEPT SKETCHES.
These are rough, first-draft ideas that have potential but need your creative vision.

For EACH concept sketch, create an ENHANCED VERSION that:
- Removes the boring, predictable parts
- Amplifies what makes it interesting
- Adds unexpected elements from other domains
- Makes it something people will actually remember

Structure your output as:

---
## Concept N: [Your New Title]

### Initial Sketch
[Summarize the concept you received]

### Enhanced Version
[Your transformed, amplified take - make it 10x more interesting]

### What Changed
[Brief note on what you added/removed to make it better]

---

Transform ALL concepts. Each one has hidden potential - find it.""",
        agent=agent,
        context=context,
        expected_output="A complete list of enhanced concepts, each with the initial sketch, your enhanced version, and notes on the transformation.",
    )


def create_amplification_task_2(agent, context) -> Task:
    """Create the second weirdness amplification task (also blinded)."""
    return Task(
        description="""You've received a batch of PRELIMINARY IDEAS from the ideation team.
They're okay starting points, but they're playing it way too safe.

Your mission: Take each preliminary idea and CREATE THE UNHINGED VERSION.

For each idea, ask yourself:
- What if we went 10x further?
- What would the fever dream version look like?
- What if we combined this with something completely incompatible?
- What would make this idea LEGENDARY?
- What version would people still talk about in 20 years?

Structure your output as:

---
## Idea N: [Your Bold New Title]

### Preliminary Version
[The idea as you received it]

### MAXIMUM CHAOS VERSION
[Your wildest, most unhinged interpretation - remove ALL guardrails]

### The Transformation
[What pushed this from "interesting" to "unforgettable"?]

---

Do this for EVERY SINGLE IDEA. No exceptions. No playing it safe.
The goal is to make the preliminary versions look boring by comparison.""",
        agent=agent,
        context=context,
        expected_output="A complete list showing preliminary ideas transformed into their most experimental, memorable, unhinged versions.",
    )


def create_evaluation_task(agent, context) -> Task:
    """Create the idea evaluation task."""
    return Task(
        description="""Evaluate each AI experiment idea on the following criteria:

1. **Creativity Score (1-10)**: How original and innovative is this idea?
2. **Feasibility Score (1-10)**: How realistic is it to implement with current technology?
3. **Uniqueness Score (1-10)**: How different is this from other ideas in the list?
4. **Impact Score (1-10)**: What potential value or insights could this provide?
5. **Overall Score**: Average of the above scores

For each idea, provide:
- Scores for each criterion
- Brief justification for scores
- Identification of any ideas that are too similar to each other
- Highlight of the top 10 most promising ideas

Create a summary analysis identifying:
- Patterns in the idea generation
- Diversity assessment of the entire set
- Any gaps or underexplored areas
- Recommendations for which ideas to prioritize""",
        agent=agent,
        context=context,
        expected_output="A comprehensive evaluation of all ideas with scores, justifications, similarity analysis, top 10 highlights, and strategic recommendations.",
    )


def create_categorization_task(agent, context) -> Task:
    """Create the idea categorization task."""
    return Task(
        description="""Organize all AI experiment ideas into meaningful thematic categories.

Your categorization should:
1. Create 5-10 high-level categories that capture the main themes
2. Assign each idea to one or more categories (ideas can belong to multiple categories)
3. Identify subcategories where appropriate
4. Look for cross-cutting themes (e.g., "uses multi-agent systems", "involves physical world", "artistic focus")

For each category, provide:
- Category name and description
- List of ideas that belong to it
- Key characteristics of ideas in this category
- Potential synergies between ideas in the category

Also provide:
- A visual-friendly category tree structure
- Identification of the most and least populated categories
- Suggestions for categories that could be expanded in future ideation sessions""",
        agent=agent,
        context=context,
        expected_output="A well-organized taxonomy of all ideas with clear categories, subcategories, cross-cutting themes, and strategic insights about the idea landscape.",
    )


def create_synthesis_task(agent, context) -> Task:
    """Create the final synthesis and reporting task."""
    return Task(
        description="""Create a comprehensive final report that synthesizes all the work:

Your report should include:

1. **Executive Summary**
   - Overview of the ideation process
   - Key statistics (number of ideas, categories, etc.)
   - Highlight of most notable ideas

2. **Top Ideas Showcase**
   - Detailed presentation of the top 10-15 ideas
   - Why they stand out
   - Implementation roadmap for the most promising ones

3. **Thematic Analysis**
   - Overview of all categories
   - Trends and patterns observed
   - Connections between seemingly different ideas

4. **Diversity Assessment**
   - How well did we avoid repetition?
   - Which domains were well-covered vs. underexplored?
   - Suggestions for future ideation sessions

5. **Feasibility Tiers**
   - Quick wins: Easy experiments that could be done soon
   - Medium-term projects: More complex but achievable
   - Long-term visions: Ambitious ideas requiring significant resources

6. **Commercial Opportunities**
   - Ideas with clear market potential
   - Potential business models
   - Market niches that could be served

7. **Recommendations**
   - Which experiments to prioritize
   - Resource allocation suggestions
   - Next steps for moving from ideas to implementation

Make the report engaging, well-structured, and actionable. Use markdown formatting for clarity.""",
        agent=agent,
        context=context,
        expected_output="A comprehensive, well-formatted markdown report synthesizing all findings with executive summary, top ideas, thematic analysis, feasibility assessment, commercial opportunities, and actionable recommendations.",
    )
