"""Main crew orchestration for the Weird AI Experiment Ideator."""
from dataclasses import dataclass
from typing import Dict, Any
from crewai import Crew, Process
from .agents import (
    create_generator_agent,
    create_amplifier_agent_1,
    create_amplifier_agent_2,
    create_evaluator_agent,
    create_categorizer_agent,
    create_synthesizer_agent,
)
from .tasks import (
    create_generation_task,
    create_amplification_task_1,
    create_amplification_task_2,
    create_evaluation_task,
    create_categorization_task,
    create_synthesis_task,
)


@dataclass
class IdeationResult:
    """Container for all ideation session outputs."""
    generation_output: str
    amplification_1_output: str  # First pass (blinded)
    amplification_2_output: str  # Second pass (also blinded - MAXIMUM CHAOS)
    evaluation_output: str
    categorization_output: str
    synthesis_output: str
    final_result: Any

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "generation_output": self.generation_output,
            "amplification_1_output": self.amplification_1_output,
            "amplification_2_output": self.amplification_2_output,
            "evaluation_output": self.evaluation_output,
            "categorization_output": self.categorization_output,
            "synthesis_output": self.synthesis_output,
            "final_result": str(self.final_result),
        }


def create_ideation_crew() -> tuple:
    """Create and configure the multi-agent crew. Returns (crew, tasks_dict)."""

    # Create agents
    generator = create_generator_agent()
    amplifier_1 = create_amplifier_agent_1()  # First weirdness pass
    amplifier_2 = create_amplifier_agent_2()  # Second weirdness pass (MAXIMUM CHAOS)
    evaluator = create_evaluator_agent()
    categorizer = create_categorizer_agent()
    synthesizer = create_synthesizer_agent()

    # Create tasks in sequence - each amplifier only sees the previous output (blinded)
    generation_task = create_generation_task(generator)
    amplification_task_1 = create_amplification_task_1(amplifier_1, [generation_task])
    # Second amplifier only sees first amplification output - doesn't know it's already been amplified!
    amplification_task_2 = create_amplification_task_2(amplifier_2, [amplification_task_1])
    # Evaluator and categorizer see all versions
    evaluation_task = create_evaluation_task(evaluator, [generation_task, amplification_task_1, amplification_task_2])
    categorization_task = create_categorization_task(categorizer, [generation_task, amplification_task_1, amplification_task_2])
    synthesis_task = create_synthesis_task(
        synthesizer,
        [generation_task, amplification_task_1, amplification_task_2, evaluation_task, categorization_task]
    )

    # Store tasks for later output retrieval
    tasks_dict = {
        "generation": generation_task,
        "amplification_1": amplification_task_1,
        "amplification_2": amplification_task_2,
        "evaluation": evaluation_task,
        "categorization": categorization_task,
        "synthesis": synthesis_task,
    }

    # Create crew with sequential process
    crew = Crew(
        agents=[generator, amplifier_1, amplifier_2, evaluator, categorizer, synthesizer],
        tasks=[generation_task, amplification_task_1, amplification_task_2, evaluation_task, categorization_task, synthesis_task],
        process=Process.sequential,
        verbose=True,
    )

    return crew, tasks_dict


def run_ideation_session() -> IdeationResult:
    """Run a complete ideation session and return ALL outputs."""
    print("🚀 Starting Weird AI Experiment Ideation Session...")
    print("=" * 80)
    print("Pipeline: Generator → Amplifier #1 (blinded) → Amplifier #2 (blinded) → Evaluator → Categorizer → Synthesizer")
    print("=" * 80)

    crew, tasks_dict = create_ideation_crew()
    result = crew.kickoff()

    print("=" * 80)
    print("✅ Ideation session complete!")

    # Extract individual task outputs
    ideation_result = IdeationResult(
        generation_output=str(tasks_dict["generation"].output) if tasks_dict["generation"].output else "",
        amplification_1_output=str(tasks_dict["amplification_1"].output) if tasks_dict["amplification_1"].output else "",
        amplification_2_output=str(tasks_dict["amplification_2"].output) if tasks_dict["amplification_2"].output else "",
        evaluation_output=str(tasks_dict["evaluation"].output) if tasks_dict["evaluation"].output else "",
        categorization_output=str(tasks_dict["categorization"].output) if tasks_dict["categorization"].output else "",
        synthesis_output=str(tasks_dict["synthesis"].output) if tasks_dict["synthesis"].output else "",
        final_result=result,
    )

    return ideation_result
