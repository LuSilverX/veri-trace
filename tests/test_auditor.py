import pytest
import os
import json
import tempfile
from auditor import TrajectoryAuditor
from agent import VerifiedResponse

class TestTrajectoryAuditor:
    def test_init(self):
        auditor = TrajectoryAuditor()
        assert auditor.logs == []

    def test_record_step(self):
        auditor = TrajectoryAuditor()
        # Mock a VerifiedResponse
        mock_output = VerifiedResponse(
            reasoning_steps=["Step 1", "Step 2"],
            answer="Final answer",
            confidence=0.9
        )
        auditor.record_step(1, mock_output, True)
        assert len(auditor.logs) == 1
        log = auditor.logs[0]
        assert log["attempt"] == 1
        assert log["reasoning"] == ["Step 1", "Step 2"]
        assert log["answer"] == "Final answer"
        assert log["audit_passed"] == True

    def test_save_report(self):
        auditor = TrajectoryAuditor()
        mock_output = VerifiedResponse(
            reasoning_steps=["Reasoning"],
            answer="Answer",
            confidence=1.0
        )
        auditor.record_step(1, mock_output, False)

        # Use a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            try:
                auditor.save_report()
                # Check if logs directory was created
                assert os.path.exists("logs")
                # Check if a json file was created
                json_files = [f for f in os.listdir("logs") if f.endswith(".json")]
                assert len(json_files) == 1
                with open(os.path.join("logs", json_files[0]), "r") as f:
                    data = json.load(f)
                    assert len(data) == 1
                    assert data[0]["attempt"] == 1
            finally:
                os.chdir(original_cwd)