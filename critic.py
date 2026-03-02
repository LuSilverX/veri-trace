import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from agent import VerifiedResponse  

load_dotenv()

# The 'Judge' or 'Red-Teamer'
critic = Agent(
    'google-gla:gemini-2.5-flash',
    output_type=bool, # The Critic just gives a Thumb Up (True) or Thumb Down (False)
    system_prompt="""
    You are a Senior Logic Auditor. Your job is to review an Agent's reasoning.
    Look for:
    1. Circular logic.
    2. Mathematical errors.
    3. Failure to account for parallel processes (like the towel drying problem).
    
    If the logic is 100% sound, return True. 
    If there is ANY flaw, return False.
    """
)

def audit_agent_response(agent_output: VerifiedResponse):
    print(f"\n🔍 AUDITING LOGIC...")
    
    # Passing the Agent's reasoning steps to the Critic
    audit_input = f"Reasoning to Audit: {agent_output.reasoning_steps} | Final Answer: {agent_output.answer}"
    
    result = critic.run_sync(audit_input)
    
    if result.output is True:
        print("✅ LOGIC VERIFIED: The Critic found no flaws.")
    else:
        print("❌ LOGIC REJECTED: The Critic found a logical fallacy!")
    
    return result.output