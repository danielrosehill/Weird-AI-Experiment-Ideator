"""Data models for structured idea output."""
from pydantic import BaseModel, Field
from typing import List, Optional


class AIExperimentIdea(BaseModel):
    """Structured representation of an AI experiment idea."""

    id: int = Field(description="Unique identifier for the idea (1-N)")
    title: str = Field(description="Catchy, descriptive title for the experiment")
    elevator_pitch: str = Field(
        description="One-sentence hook that captures the essence (max 200 chars)",
        max_length=200
    )
    description: str = Field(
        description="Detailed explanation of what the experiment is and how it works"
    )
    implementation: str = Field(
        description="Technical approach, tools needed, and step-by-step implementation guide"
    )
    feasibility: str = Field(
        description="Realistic assessment of difficulty, resources required, and timeline"
    )
    potential_impact: str = Field(
        description="What might be learned, achieved, or discovered through this experiment"
    )
    commercial_viability: Optional[str] = Field(
        default=None,
        description="Market potential and business model, if applicable"
    )
    domain: List[str] = Field(
        description="Domains this idea spans (e.g., 'AI', 'Art', 'Education', 'Robotics')"
    )
    ai_technologies: List[str] = Field(
        description="AI technologies used (e.g., 'LLM', 'Computer Vision', 'Multi-Agent')"
    )


class IdeaEvaluation(BaseModel):
    """Evaluation scores and analysis for an idea."""

    idea_id: int
    creativity_score: int = Field(ge=1, le=10)
    feasibility_score: int = Field(ge=1, le=10)
    uniqueness_score: int = Field(ge=1, le=10)
    impact_score: int = Field(ge=1, le=10)
    overall_score: float = Field(description="Average of all scores")
    justification: str = Field(description="Brief explanation of the scores")
    similar_to: Optional[List[int]] = Field(
        default=None,
        description="IDs of similar ideas, if any"
    )


class IdeaCategory(BaseModel):
    """A thematic category grouping related ideas."""

    name: str = Field(description="Category name")
    description: str = Field(description="What this category represents")
    idea_ids: List[int] = Field(description="IDs of ideas in this category")
    key_characteristics: str = Field(
        description="Common traits of ideas in this category"
    )


class IdeationSession(BaseModel):
    """Complete ideation session output."""

    timestamp: str
    num_ideas: int
    ideas: List[AIExperimentIdea]
    evaluations: List[IdeaEvaluation]
    categories: List[IdeaCategory]
    top_ideas: List[int] = Field(description="IDs of top-rated ideas")
    summary: str = Field(description="Executive summary of the session")


class BatchIdea(BaseModel):
    """Simplified format for batch PDF generation."""

    title: str
    elevator_pitch: str
    full_description: str = Field(
        description="Combined description, implementation, and impact"
    )
    scores: Optional[dict] = Field(
        default=None,
        description="Evaluation scores if available"
    )
