import os
import time
import types
from collections.abc import Iterator
from typing import Any, Dict, List, Optional, TYPE_CHECKING

import ulid

from ..serialize import get_callsite_data, serialize_query_data


if TYPE_CHECKING:
    # Literal and TypedDict only exist on python 3.8+
    # We run mypy using a high enough version, so this is ok!
    from typing import Literal, TypedDict
    from ..serialize import UserCodeCallSite

    class QueryStart(TypedDict):
        frame_id: str
        query_template: str
        user_code_call_site: Optional[UserCodeCallSite]
        call_timestamp: float
        timestamp: float
        type: Literal["start_sql_query"]

    class QueryEnd(TypedDict, total=False):
        frame_id: str
        query: str
        query_template: str
        return_timestamp: float
        timestamp: float
        type: Literal["end_sql_query"]

    class QueryData(TypedDict):
        frame_id: str
        query_data: Optional[List[Any] | str]
        query_template: str
        timestamp: float
        type: Literal["sql_query_data"]


class SQLQueryFilter:
    co_names = ["_execute", "execute_sql"]

    def __init__(self, config) -> None:
        self.config = config
        self._frame_ids: Dict[int, str] = {}

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        co_name = frame.f_code.co_name
        filename = frame.f_code.co_filename
        return (
            co_name == "_execute"
            and os.path.normpath("/django/db/backends/utils.py") in filename
        ) or (
            event == "return"
            and co_name == "execute_sql"
            and os.path.normpath("/django/db/models/sql/compiler.py") in filename
        )

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: Any,
        call_frame_ids: List[Dict[str, str]],
    ):
        timestamp = time.time()
        co_name = frame.f_code.co_name
        if co_name == "_execute":
            if event == "call":
                frame_id = f"frm_{ulid.new()}"
                self._frame_ids[id(frame)] = frame_id
                if call_frame_ids:
                    user_code_call_site = get_callsite_data(frame, call_frame_ids[-1])
                else:
                    user_code_call_site = None

                query_start: QueryStart = {
                    "frame_id": frame_id,
                    "user_code_call_site": user_code_call_site,
                    "call_timestamp": time.time(),
                    "query_template": frame.f_locals["sql"].strip(),
                    "timestamp": timestamp,
                    "type": "start_sql_query",
                }
                return query_start

            assert event == "return"
            ops = frame.f_locals["self"].db.ops
            cursor = frame.f_locals["self"].cursor
            sql = frame.f_locals["sql"]
            params = frame.f_locals["params"]
            query_end: QueryEnd = {
                "frame_id": self._frame_ids[id(frame)],
                "return_timestamp": timestamp,
                "query_template": sql.strip(),
                "query": ops.last_executed_query(cursor, sql, params).strip(),
                "timestamp": timestamp,
                "type": "end_sql_query",
            }
            return query_end

        assert co_name == "execute_sql"
        assert event == "return"

        result_type = frame.f_locals.get("result_type")
        data: Optional[List[Any] | str]
        if result_type == "cursor":
            data = "<cursor>"  # pragma: no cover
        else:
            if isinstance(arg, Iterator):
                data = "<consumable iterator>"  # pragma: no cover
            else:
                data = serialize_query_data(arg)

        sql = frame.f_locals["sql"]
        params = frame.f_locals["params"]
        query_data: QueryData = {
            "frame_id": f"frm_{ulid.new()}",
            "query_template": sql.strip(),
            "query_data": data,
            "timestamp": timestamp,
            "type": "sql_query_data",
        }
        return query_data
