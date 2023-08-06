import os
import time
import types
from contextlib import suppress
from typing import Dict, List

import ulid

from ..serialize import get_content, get_request_body, serialize_locals


class DjangoFilter:
    co_names = ["get_response"]

    def __init__(self, config) -> None:
        self.config = config
        self.timestamp: float
        self._frame_ids: Dict[int, str] = {}

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        co_name = frame.f_code.co_name
        filename = frame.f_code.co_filename
        return (
            co_name == "get_response"
            and os.path.normpath("/kolo/middleware.py") in filename
        )

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        if event == "call":
            frame_id = f"frm_{ulid.new()}"
            self._frame_ids[id(frame)] = frame_id
            self.timestamp = time.time()
            request = frame.f_locals["request"]
            self.request_data = {
                "body": get_request_body(request),
                "frame_id": frame_id,
                "headers": dict(request.headers),
                "method": request.method,
                "path_info": request.path_info,
                "post_data": dict(request.POST),
                "query_params": dict(request.GET),
                "scheme": request.scheme,
                "timestamp": self.timestamp,
                "type": "django_request",
                "url_pattern": None,
            }
            return self.request_data
        elif event == "return":  # pragma: no branch
            timestamp = time.time()
            duration = timestamp - self.timestamp
            ms_duration = round(duration * 1000, 2)

            request = frame.f_locals["request"]
            match = request.resolver_match
            if match:  # match is None if this is a 404
                self.request_data["url_pattern"] = {
                    "namespace": match.namespace,
                    "route": match.route,
                    "url_name": match.url_name,
                    "view_qualname": match._func_path,
                }

            response = frame.f_locals["response"]
            return {
                "frame_id": self._frame_ids[id(frame)],
                "ms_duration": ms_duration,
                "status_code": response.status_code,
                "content": get_content(response),
                "headers": dict(response.items()),
                "timestamp": timestamp,
                "type": "django_response",
            }


class DjangoTemplateFilter:
    co_names = ["render"]

    def __init__(self, config) -> None:
        self.config = config
        self.timestamp: float
        self._frame_ids: Dict[int, str] = {}

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        co_name = frame.f_code.co_name
        filename = frame.f_code.co_filename
        return (
            co_name == "render"
            and os.path.normpath("django/template/backends/django.py") in filename
        )

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        timestamp = time.time()
        context = frame.f_locals["context"]
        with suppress(AttributeError):
            context = context.flatten()
        if event == "call":
            frame_id = f"frm_{ulid.new()}"
            self._frame_ids[id(frame)] = frame_id
            _type = "django_template_start"
        else:
            frame_id = self._frame_ids[id(frame)]
            _type = "django_template_end"

        return {
            "context": serialize_locals(context),
            "frame_id": frame_id,
            "template": frame.f_locals["self"].template.name,
            "timestamp": timestamp,
            "type": _type,
        }
