from agent.llm.qwen import get_qwen
from agent.prompts import INVESTIGATION_SYSTEM_PROMPT
from agent.workflows.lost_found_workflow import (
    InvestigationWorkflow,
)



class LostFoundAgent:
    """
    Main Lost and Found Investigation Agent.

    Qwen3 provides reasoning and natural-language interaction.
    The investigation workflow performs the actual tool-based
    investigation.
    """

    def __init__(self):
        self.llm = get_qwen()
        self.system_prompt = INVESTIGATION_SYSTEM_PROMPT

        self.workflow = InvestigationWorkflow()

    def investigate(
        self,
        lost_item_id: int,
    ) -> dict:
        """
        Start an investigation for a specific lost item.
        """

        return self.workflow.investigate(
            lost_item_id
        )

    def ask(
        self,
        question: str,
    ) -> str:
        """
        Ask Qwen3 a general investigation-related question.
        """

        response = self.llm.invoke(
            [
                (
                    "system",
                    self.system_prompt,
                ),
                (
                    "human",
                    question,
                ),
            ]
        )

        return response.content

    def get_memory(self) -> dict:
        """
        Return the current investigation memory.
        """

        return self.workflow.memory.get_context()

    