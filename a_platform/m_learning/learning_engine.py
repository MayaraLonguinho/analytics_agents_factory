import os
import json
from datetime import datetime

class LearningEngine:
    def __init__(self):
        self.learning_dir = "a_platform/m_learning/memories"
        os.makedirs(self.learning_dir, exist_ok=True)

    def record_failure(self, project_id: str, error_details: dict):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{self.learning_dir}/{project_id}_{timestamp}_failure.json"
        try:
            with open(filename, "w") as f:
                json.dump(error_details, f, indent=2)
        except Exception:
            pass
