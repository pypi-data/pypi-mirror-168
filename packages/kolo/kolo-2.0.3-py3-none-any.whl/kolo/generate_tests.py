import json

from jinja2 import Environment, PackageLoader

from .config import load_config
from .db import load_trace_from_db, setup_db


env = Environment(loader=PackageLoader("kolo"))


def _format_header(header: str) -> str:
    header = header.upper().replace("-", "_")
    if header in ("CONTENT_LENGTH", "CONTENT_TYPE"):
        return header
    return f"HTTP_{header}"


def generate_from_trace_id(trace_id: str, test_class: str, test_name: str) -> str:
    config = load_config()
    wal_mode = config.get("wal_mode", True)
    db_path = setup_db(config)
    raw_data = load_trace_from_db(db_path, trace_id, wal_mode=wal_mode)
    data = json.loads(raw_data)
    frames = data["frames_of_interest"]

    request_frames = []
    current_request = None
    for frame in frames:
        if frame["type"] == "django_request":
            current_request = {"request": frame, "templates": []}
            request_frames.append(current_request)
        elif frame["type"] == "django_response":
            assert current_request is not None
            current_request["response"] = frame
            current_request = None
        elif frame["type"] == "django_template_start":
            assert current_request is not None
            current_request["templates"].append(frame["template"])

    request = request_frames[0]["request"]
    query_params = request["query_params"]
    query_params = f"{query_params}," if query_params else ""
    post_data = request["post_data"]
    post_data = f"{post_data}," if request["method"] == "POST" else ""
    request_headers = {
        _format_header(header): value for header, value in request["headers"].items()
    }
    if "HTTP_COOKIE" in request_headers and request_headers["HTTP_COOKIE"] == "":
        del request_headers["HTTP_COOKIE"]
    if "CONTENT_LENGTH" in request_headers:
        del request_headers["CONTENT_LENGTH"]
    if "CONTENT_TYPE" in request_headers:
        del request_headers["CONTENT_TYPE"]
    response = request_frames[0]["response"]
    template = env.get_template("django_request_test.py.j2")
    rendered = template.render(
        request=request,
        response=response,
        test_class=test_class,
        test_name=test_name,
        request_headers=request_headers,
        post_data=post_data,
        query_params=query_params,
        template_names=request_frames[0]["templates"],
    )
    try:
        from black import format_file_contents
        from black.mode import Mode
    except ImportError:  # pragma: no cover
        pass
    else:
        rendered = format_file_contents(
            rendered, fast=True, mode=Mode(magic_trailing_comma=False)
        )
    return rendered
