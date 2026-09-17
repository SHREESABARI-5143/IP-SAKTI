import time
from typing import Dict, Any

class PipelineTimer:
    """
    Micro-second precision pipeline stage timer for RAG latency profiling.
    """
    def __init__(self):
        self.stages: Dict[str, float] = {}
        self._stage_starts: Dict[str, float] = {}
        self.start_total = time.perf_counter()

    def start_stage(self, stage_name: str):
        self._stage_starts[stage_name] = time.perf_counter()

    def end_stage(self, stage_name: str):
        if stage_name in self._stage_starts:
            duration_ms = (time.perf_counter() - self._stage_starts[stage_name]) * 1000.0
            self.stages[stage_name] = round(duration_ms, 2)

    def get_summary(self) -> Dict[str, Any]:
        total_ms = (time.perf_counter() - self.start_total) * 1000.0
        return {
            "total_ms": round(total_ms, 2),
            "stage_breakdown_ms": self.stages
        }
