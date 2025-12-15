"""Main crew orchestration for the Weird AI Experiment Ideator."""
from crewai import Crew, Process
from .agents import (
    create_generator_agent,
    create_evaluator_agent,
    create_categorizer_agent,
    create_synthesizer_agent,
)
from .tasks import (
    create_generation_task,
    create_evaluation_task,
    create_categorization_task,
    create_synthesis_task,
)


def create_ideation_crew() -> Crew:
    """Create and configure the multi-agent crew."""

    # Create agents
    generator = create_generator_agent()
    evaluator = create_evaluator_agent()
    categorizer = create_categorizer_agent()
    synthesizer = create_synthesizer_agent()

    # Create tasks
    generation_task = create_generation_task(generator)
    evaluation_task = create_evaluation_task(evaluator, [generation_task])
    categorization_task = create_categorization_task(categorizer, [generation_task])
    synthesis_task = create_synthesis_task(
        synthesizer,
        [generation_task, evaluation_task, categorization_task]
    )

    # Create crew with sequential process
    crew = Crew(
        agents=[generator, evaluator, categorizer, synthesizer],
        tasks=[generation_task, evaluation_task, categorization_task, synthesis_task],
        process=Process.sequential,
        verbose=True,
    )

    return crew


def run_ideation_session() -> str:
    """Run a complete ideation session and return the final report."""
    print("🚀 Starting Weird AI Experiment Ideation Session...")
    print("=" * 80)

    crew = create_ideation_crew()
    result = crew.kickoff()

    print("=" * 80)
    print("✅ Ideation session complete!")

    return result
