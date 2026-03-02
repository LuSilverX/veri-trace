import os
import time
import json
from datetime import datetime

class TrajectoryAuditor:
    def __init__(self):
        self.logs = []

    def record_step(self, attempt: int, agent_output, audit_result: bool):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "attempt": attempt,
            "reasoning": agent_output.reasoning_steps,
            "answer": agent_output.answer,
            "audit_passed": audit_result
        }
        self.logs.append(log_entry)
        print(f"📊 [AUDITOR]: Attempt {attempt} recorded.")

    def save_report(self):
        os.makedirs("logs", exist_ok=True)
        filename = f"logs/trace_{int(time.time())}.json"
        with open(filename, "w") as f:
            json.dump(self.logs, f, indent=4)
        print(f"💾 [AUDITOR]: Final report saved to {filename}")