import os
import time
from typing import Dict

import ulid


class PytestFilter:
    event_types = {
        "pytest_runtest_logstart": "start_test",
        "pytest_runtest_logfinish": "end_test",
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
            and co_name in self.event_types
            and os.path.normpath("kolo/pytest_plugin.py") in filepath
        )

    def process(self, frame, event, arg, call_frame_ids):  # pragma: no cover
        timestamp = time.time()
        co_name = frame.f_code.co_name
        location = frame.f_locals["location"]
        if co_name == "pytest_runtest_logstart":
            frame_id = f"frm_{ulid.new()}"
            self._frame_ids[id(location)] = frame_id
        else:
            frame_id = self._frame_ids[id(location)]

        filename, lineno, test = location
        test_class, _sep, test_name = test.rpartition(".")
        return {
            "frame_id": frame_id,
            "type": self.event_types[co_name],
            "test_name": test_name,
            "test_class": test_class if test_class else None,
            "timestamp": timestamp,
        }
