from __future__ import annotations

from typing import Any, NamedTuple

from jsonpath_ng import parse


class ExtractReq(NamedTuple):
    jsonpath: str
    alias: str | None = None


class ExtractResp(NamedTuple):
    jsonpath: str
    value: Any


def extract(extract_req: ExtractReq, d: dict[str, Any]) -> ExtractResp | None:
    try:
        match = parse(extract_req.jsonpath).find(d)[0]
    except IndexError:
        return None

    return ExtractResp(
        jsonpath=str(match.path),
        value=match.value,
    )
