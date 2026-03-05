import os
from dotenv import load_dotenv
from agent import agent
from critic import audit_agent_response
from auditor import TrajectoryAuditor
from reporter import generate_markdown_report

load_dotenv()

def run_veritrace_loop(user_question: str, max_retries: int = 3):
    print(f"\n🚀 STARTING TRACE: {user_question}")
    
    auditor = TrajectoryAuditor()
    current_attempt = 1
    feedback = ""

    while current_attempt <= max_retries:
        print(f"\n--- ATTEMPT {current_attempt} ---")
        
        # 1. Ask the Agent (we pass feedback if this is a retry)
        prompt = user_question
        if feedback:
            prompt = f"{user_question}\n\nPREVIOUS CRITIQUE: {feedback}\nPlease fix your logic based on this feedback."

        result = agent.run_sync(prompt)
        
        # 2. Audit the response
        is_valid = audit_agent_response(result.output)
        
        # 3. Record the step in the auditor
        auditor.record_step(current_attempt, result.output, is_valid)

        if is_valid:
            print("\n🏁 FINAL VERIFIED RESULT:")
            print(result.output.answer)
            auditor.save_report()
            generate_markdown_report()
            return result.output
        else:
            feedback = "The logic was flagged as flawed. Please re-evaluate the constraints of the problem."
            current_attempt += 1

    auditor.save_report()
    generate_markdown_report()
    print("\n🛑 TRACE FAILED: Could not verify logic within retry limit.")
    return None

if __name__ == "__main__":
    # The "Towel Problem" is the classic test for logic vs. pattern matching
    question = "If it takes 3 towels 3 hours to dry in the sun, how long does it take 6 towels?"
    run_veritrace_loop(question)