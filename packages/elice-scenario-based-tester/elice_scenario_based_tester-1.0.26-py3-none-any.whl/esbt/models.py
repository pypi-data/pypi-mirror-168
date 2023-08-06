from __future__ import annotations

import asyncio
import re
import time
from typing import Any, Literal

from esbt.ctx import StoreKey, WorkflowCtx, bind_workflow_ctx

from .utils import misc as misc_utils

_FORMAT_STR_RE = re.compile(r'{(?P<value>[a-zA-Z_]+)}')
_SCN_DEPENDENCY_WAIT_TIMEOUT = 1 * 60  # 1 minute


class ESBTException(Exception):
    pass


class Request:
    def __init__(
        self,
        method: Literal['POST', 'GET'],
        path: str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        filename_to_path: dict[str, str] | None = None,
        extract_req_list: list[misc_utils.ExtractReq] | None = None,
    ) -> None:
        self.method = method
        self.path = path
        self.params = params
        self.data = data
        self.headers = headers
        self.filename_to_path = filename_to_path
        self.extract_req_list = extract_req_list

        self._filename_to_fp: dict[str, Any] = {}

    async def run(self) -> None:
        try:
            self._open_file()

            resp_raw = await WorkflowCtx.current.session.request(
                method=self.method,
                url=WorkflowCtx.current.settings.API_ENDPOINT + self.path,
                headers=self._repl(self.headers),
                data=self._repl(self.data),
                params=self._repl(self.params),
            )

            if not 200 <= resp_raw.status < 300:
                raise ESBTException('Not successful status code')

            resp_json = await resp_raw.json()

            self._verify_resp(resp_json)

            self._save_to_store(resp_json)
        finally:
            self._close_file()

    def _verify_resp(self, d: dict[str, Any]) -> None:
        for jsonpath, val in WorkflowCtx.current.settings.RESPONSE_VERIFY_DICT.items():
            extract_resp = misc_utils.extract(
                misc_utils.ExtractReq(jsonpath=jsonpath),
                d,
            )

            if extract_resp is None:
                raise ESBTException('No matching key in the response')

            if extract_resp.value != val:
                raise ESBTException('Invalid response')

    def _open_file(self) -> dict[str, Any]:
        filename_to_fp = self._filename_to_fp = {
            filename: open(filepath, 'rb')
            for filename, filepath in (self.filename_to_path or {}).items()
        }

        self.data = {
            **(self.data or {}),
            **filename_to_fp,
        }

        return filename_to_fp

    def _close_file(self) -> None:
        for fp in self._filename_to_fp.values():
            fp.close()

    def _save_to_store(self, d: dict[str, Any]) -> None:
        for extract_req in self.extract_req_list or []:
            extract_resp = misc_utils.extract(extract_req, d)

            if extract_resp is None:
                raise ESBTException('No matching key in the response')

            WorkflowCtx.current.save_to_store(
                store_key=StoreKey(
                    agent_name=WorkflowCtx.current.agent_name,
                    scn_cls=WorkflowCtx.current.scn_cls,
                    repeat_pos=WorkflowCtx.current.repeat_pos,
                    name=extract_req.alias or extract_resp.jsonpath,
                ),
                value=extract_resp.value,
            )

    def _repl(self, d: dict[str, Any] | None) -> dict[str, Any]:
        if d is None:
            return {}

        new_d = {**d}

        for key, value in d.items():
            if not isinstance(value, str):
                continue

            re_m = _FORMAT_STR_RE.search(value)

            if re_m is None:
                continue

            for store_key in [
                *[
                    StoreKey(
                        agent_name=dependency_item.agent_name,
                        scn_cls=dependency_item.scn_cls,
                        repeat_pos=repeat_pos,
                        name=re_m.group('value'),
                    )
                    for dependency_item in WorkflowCtx.current.dependency_item_list
                    for repeat_pos in range(WorkflowCtx.current.repeat_pos or 0 + 1)
                ],
                *[
                    StoreKey(
                        agent_name=WorkflowCtx.current.agent_name,
                        scn_cls=scn.__class__,
                        repeat_pos=repeat_pos,
                        name=re_m.group('value'),
                    )
                    for scn in WorkflowCtx.current.agent_scns
                    for repeat_pos in reversed(range(scn.repeat_cnt))
                ],
            ]:
                store_value = WorkflowCtx.current.get_from_store(store_key)

                if store_value is not None:
                    value = re_m.re.sub(str(store_value), value)
                    break
            else:
                raise ESBTException('No matching key in the workflow store')

            new_d[key] = value

        return new_d


class ScnBase:
    requests: list[Request]

    def __init__(self, *, repeat_cnt: int = 1) -> None:
        self.repeat_cnt = repeat_cnt

    async def run(self) -> None:
        start_time = time.monotonic()
        while time.monotonic() - start_time < _SCN_DEPENDENCY_WAIT_TIMEOUT:
            is_completed = all(
                WorkflowCtx.current.has_store_key(
                    StoreKey(
                        agent_name=dependency_item.agent_name,
                        scn_cls=dependency_item.scn_cls,
                        repeat_pos=None,
                        name='is_completed',
                    )
                )
                for dependency_item in WorkflowCtx.current.dependency_item_list
            )

            if is_completed:
                break
            else:
                await asyncio.sleep(.5)
        else:
            raise ESBTException('the dependent scenarios do not completed in time')

        for repeat_pos in range(self.repeat_cnt):
            for request in self.requests:
                async with bind_workflow_ctx(
                    WorkflowCtx.current,
                    agent=WorkflowCtx.current.agent,
                    scn=WorkflowCtx.current.scn,
                    repeat_pos=repeat_pos,
                ):
                    await request.run()

        WorkflowCtx.current.save_to_store(
            store_key=StoreKey(
                agent_name=WorkflowCtx.current.agent_name,
                scn_cls=WorkflowCtx.current.scn_cls,
                repeat_pos=None,
                name='is_completed',
            ),
            value=True,
        )


class Agent:
    def __init__(self, name: str, scns: list[ScnBase]) -> None:
        self.name = name
        self.scns = scns

    async def run(self) -> None:
        for scn in self.scns:
            async with bind_workflow_ctx(
                WorkflowCtx.current,
                agent=self,
                scn=scn,
            ):
                await scn.run()
