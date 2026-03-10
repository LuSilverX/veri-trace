import os
import sys
from dotenv import load_dotenv
from agent import agent
from critic import audit_agent_response
from auditor import TrajectoryAuditor
from reporter import generate_markdown_report

load_dotenv()

def run_veritrace_loop(user_question: str, max_retries: int = 3):
    """
    Orchestrates the Agent-Critic loop for a single question.
    Returns the verified result or None if max retries are reached.
    """
    print(f"\n🚀 STARTING TRACE: {user_question}")
    
    auditor = TrajectoryAuditor()
    current_attempt = 1
    feedback = ""

    while current_attempt <= max_retries:
        print(f"\n--- ATTEMPT {current_attempt} ---")
        
        # 1. Ask the Agent (inject feedback on retries)
        prompt = user_question
        if feedback:
            prompt = f"{user_question}\n\nPREVIOUS CRITIQUE: {feedback}\nPlease fix your logic based on this feedback."

        try:
            result = agent.run_sync(prompt)
        except Exception as e:
            print(f"❌ API Error: {e}")
            return None
        
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
            print("⚠️  Critic flagged a flaw. Attempting re-evaluation...")
            feedback = "The logic was flagged as flawed. Please re-evaluate the constraints of the problem."
            current_attempt += 1

    auditor.save_report()
    generate_markdown_report()
    print("\n🛑 TRACE FAILED: Could not verify logic within retry limit.")
    return None

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🛡️  VERITRACE: INTERACTIVE LOGIC AUDITOR")
    print("="*50)
    print("Type 'exit' or 'quit' to end session.")
    print("Press Ctrl+C to force stop.")

    try:
        while True:
            try:
                question = input("\n❓ Ask me ANYTHING: ").strip()
            except EOFError:
                break
                
            if not question:
                continue
            
            if question.lower() in ['exit', 'quit', 'q']:
                print("\nShutting down VeriTrace. Goodbye!")
                break
            
            run_veritrace_loop(question)
            
            print("\n" + "-"*30)
            print("Audit complete. Reports updated in /reports.")

    except KeyboardInterrupt:
        print("\n\n👋 Session ended by user. Closing threads...")
        sys.exit(0)