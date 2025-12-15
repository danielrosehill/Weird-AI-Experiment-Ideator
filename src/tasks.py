"""Task definitions for the Weird AI Experiment Ideator."""
from crewai import Task
from .config import NUM_IDEAS


def create_generation_task(agent) -> Task:
    """Create the idea generation task."""
    return Task(
        description=f"""Generate {NUM_IDEAS} unique and creative AI experiment ideas.

Each idea should:
- Be distinct and avoid repetition with other ideas
- Span different domains (art, science, entertainment, education, social experiments, etc.)
- Include both simple and complex experiments
- Cover various AI technologies (LLMs, computer vision, speech, robotics, multi-agent systems, etc.)
- Be ethical, legal, and non-harmful

For each idea, provide:
1. **Title**: A catchy, descriptive name
2. **Description**: What the experiment is and how it works
3. **Implementation**: Technical approach and tools needed
4. **Feasibility**: Realistic assessment of difficulty and resources
5. **Potential Impact**: What might be learned or achieved
6. **Commercial Viability**: If applicable, market potential

Focus on DIVERSITY. If you notice you're generating similar ideas, pivot to completely different domains.
Think broadly: embodied AI, programmatic workflows, multi-agent systems, AI in physical spaces,
AI in social contexts, AI for art, AI for science, unconventional interfaces, etc.

IMPORTANT: Number each idea clearly (1-{NUM_IDEAS}) and separate them distinctly.""",
        agent=agent,
        expected_output=f"A detailed list of {NUM_IDEAS} diverse AI experiment ideas, each with title, description, implementation details, feasibility analysis, potential impact, and commercial viability assessment.",
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
