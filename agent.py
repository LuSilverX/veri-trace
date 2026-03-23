from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent

load_dotenv()

# "Logic Guardrail" (Data Contract)
# Forcing AI to be structured.
class VerifiedResponse(BaseModel):
    reasoning_steps: list[str] = Field(description="The logical steps taken to find the answer")
    answer: str = Field(description="The final result")
    confidence: float = Field(description="0.0 to 1.0 score of certainty")

# Defining the Agent
agent = Agent(
    'google-gla:gemini-2.5-flash',
    output_type=VerifiedResponse,
    system_prompt="You are a rigorous logic engine. Break down every problem step-by-step."
)

