"""Agent definitions for the Weird AI Experiment Ideator."""
from crewai import Agent
from langchain_openai import ChatOpenAI
from .config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    GENERATOR_MODEL,
    EVALUATOR_MODEL,
    CATEGORIZER_MODEL,
    SYNTHESIZER_MODEL,
    TEMPERATURE,
)


def create_llm(model: str, temperature: float = TEMPERATURE) -> ChatOpenAI:
    """Create an LLM instance configured for OpenRouter."""
    return ChatOpenAI(
        model=model,
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base=OPENROUTER_BASE_URL,
        temperature=temperature,
    )


def create_generator_agent() -> Agent:
    """Create the idea generation agent."""
    return Agent(
        role="Weird AI Experiment Ideator",
        goal="Generate creative, diverse, and unique AI experiment ideas that push boundaries",
        backstory="""You are a wildly creative AI researcher and futurist who specializes
        in thinking of unusual, experimental, and thought-provoking uses of artificial
        intelligence. You draw inspiration from science fiction, art, sociology, psychology,
        and emerging technologies. You excel at thinking outside the box and avoiding
        repetitive or obvious ideas. Your ideas span the spectrum from practical to
        whimsical, from simple to complex, but all share a sense of wonder and curiosity
        about what AI can do.""",
        verbose=True,
        allow_delegation=False,
        llm=create_llm(GENERATOR_MODEL),
    )


def create_evaluator_agent() -> Agent:
    """Create the idea evaluation agent."""
    return Agent(
        role="AI Experiment Evaluator",
        goal="Critically assess AI experiment ideas for creativity, feasibility, uniqueness, and potential impact",
        backstory="""You are a pragmatic AI researcher with deep technical knowledge
        and a keen eye for innovation. You evaluate ideas across multiple dimensions:
        how original they are, how feasible they are to implement, what resources they'd
        require, and what value they might provide. You're not afraid to point out when
        ideas are too similar or derivative, but you also recognize genuinely novel
        approaches. Your assessments help identify the most promising experiments.""",
        verbose=True,
        allow_delegation=False,
        llm=create_llm(EVALUATOR_MODEL),
    )


def create_categorizer_agent() -> Agent:
    """Create the idea categorization agent."""
    return Agent(
        role="AI Experiment Taxonomist",
        goal="Organize AI experiment ideas into meaningful thematic categories and identify patterns",
        backstory="""You are a systematic thinker who excels at finding patterns and
        organizing information. You have a background in library science, knowledge
        management, and AI research. You can identify subtle connections between
        seemingly disparate ideas and create intuitive category structures. Your
        categorizations help people navigate large collections of ideas and discover
        unexpected relationships between concepts.""",
        verbose=True,
        allow_delegation=False,
        llm=create_llm(CATEGORIZER_MODEL),
    )


def create_synthesizer_agent() -> Agent:
    """Create the synthesis and reporting agent."""
    return Agent(
        role="AI Research Synthesizer",
        goal="Create comprehensive, insightful reports that synthesize ideas, evaluations, and categories",
        backstory="""You are a skilled technical writer and analyst who excels at
        taking complex, multifaceted information and distilling it into clear,
        actionable insights. You understand how to highlight the most important
        findings, identify trends, and present information in a way that's both
        thorough and accessible. Your reports help decision-makers understand the
        landscape of possibilities and choose the most promising directions.""",
        verbose=True,
        allow_delegation=False,
        llm=create_llm(SYNTHESIZER_MODEL),
    )
