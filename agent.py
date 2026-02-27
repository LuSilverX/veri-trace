import os
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

# Quick test run
if __name__ == "__main__":
    # We use 'sync' run for now to keep it simple (no async/await yet)
    result = agent.run_sync("If it takes 3 towels 3 hours to dry in the sun, how long does it take 6 towels?")
    
    print("--- AI REASONING ---")
    for step in result.output.reasoning_steps:
        print(f"-> {step}")
        
    print(f"\nFINAL ANSWER: {result.output.answer}")
    print(f"CONFIDENCE: {result.output.confidence}")