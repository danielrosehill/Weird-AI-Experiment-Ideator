"""Crew orchestration for the Weird AI Experiment Ideator."""
from dataclasses import dataclass
from typing import Dict, Any
from crewai import Crew, Process
from .agents import (
    create_generator_agent,
    create_reviewer_agent_1,
    create_reviewer_agent_2,
    create_synthesizer_agent,
)
from .tasks import (
    create_generation_task,
    create_review_task_1,
    create_review_task_2,
    create_synthesis_task,
)


@dataclass
class IdeationResult:
    """Container for all ideation session outputs."""
    generation_output: str
    amplified_1_output: str
    amplified_2_output: str
    final_output: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "generation": self.generation_output,
            "amplified_1": self.amplified_1_output,
            "amplified_2": self.amplified_2_output,
            "final": self.final_output,
        }


def run_ideation_session() -> IdeationResult:
    """Run complete ideation session with blinded reviews."""
    print("🎯 Starting Ideation Session")
    print("=" * 60)
    print("Pipeline: Generator → Blind Review 1 → Blind Review 2 → Builder")
    print("=" * 60)

    # Create agents
    generator = create_generator_agent()
    reviewer_1 = create_reviewer_agent_1()
    reviewer_2 = create_reviewer_agent_2()
    synthesizer = create_synthesizer_agent()

    # Create tasks - TRUE BLINDING: both reviewers see ONLY the original ideas
    # They never see each other's feedback
    gen_task = create_generation_task(generator)
    review1_task = create_review_task_1(reviewer_1, [gen_task])  # Sees only original
    review2_task = create_review_task_2(reviewer_2, [gen_task])  # Sees only original (BLINDED from review 1)
    synth_task = create_synthesis_task(synthesizer, [gen_task, review1_task, review2_task])

    tasks_dict = {
        "generation": gen_task,
        "amplified_1": review1_task,
        "amplified_2": review2_task,
        "final": synth_task,
    }

    # Run crew
    crew = Crew(
        agents=[generator, reviewer_1, reviewer_2, synthesizer],
        tasks=[gen_task, review1_task, review2_task, synth_task],
        process=Process.sequential,
        verbose=True,
    )

    crew.kickoff()

    print("=" * 60)
    print("✅ Done!")

    return IdeationResult(
        generation_output=str(tasks_dict["generation"].output) if tasks_dict["generation"].output else "",
        amplified_1_output=str(tasks_dict["amplified_1"].output) if tasks_dict["amplified_1"].output else "",
        amplified_2_output=str(tasks_dict["amplified_2"].output) if tasks_dict["amplified_2"].output else "",
        final_output=str(tasks_dict["final"].output) if tasks_dict["final"].output else "",
    )
