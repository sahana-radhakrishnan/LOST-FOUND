from agent.llm.qwen import get_qwen
from agent.prompts import INVESTIGATION_SYSTEM_PROMPT


class LostFoundAgent:
    def __init__(self):
        self.llm = get_qwen()
        self.system_prompt = INVESTIGATION_SYSTEM_PROMPT

    def ask(self, question: str):
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