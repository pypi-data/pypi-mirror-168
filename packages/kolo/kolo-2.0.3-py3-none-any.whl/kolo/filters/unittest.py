import os
import time
from typing import Dict

import ulid


class UnitTestFilter:
    event_types = {
        "startTest": "start_test",
        "stopTest": "end_test",
    }
    co_names = list(event_types)

    def __init__(self, config) -> None:
        self.config = config
        self._frame_ids: Dict[int, str] = {}

    def __call__(self, frame, event, arg):
        filepath = frame.f_code.co_filename
        co_name = frame.f_code.co_name
        return (
            event == "call"
            and os.path.normpath("unittest/result.py") in filepath
            and co_name in self.event_types
        )

    def process(self, frame, event, arg, call_frame_ids):  # pragma: no cover
        timestamp = time.time()
        testcase = frame.f_locals["test"]
        co_name = frame.f_code.co_name
        if co_name == "startTest":
            frame_id = f"frm_{ulid.new()}"
            self._frame_ids[id(testcase)] = frame_id
        else:
            frame_id = self._frame_ids[id(testcase)]
        return {
            "frame_id": frame_id,
            "type": self.event_types[co_name],
            "test_name": testcase._testMethodName,
            "test_class": testcase.__class__.__qualname__,
            "timestamp": timestamp,
        }
