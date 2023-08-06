from __future__ import annotations

from typing import TYPE_CHECKING, Dict, NamedTuple, Union

if TYPE_CHECKING:
    from aiohttp import ClientSession

    from esbt.model import ScenarioBase


class WorkflowCtx(NamedTuple):
    dependency: Dict[tuple[str, ScenarioBase], list[tuple[str, ScenarioBase]]]
    context: Dict[str, Union[str, bool]]
    session: ClientSession


def create_workflow_ctx(
    dependency: Dict[tuple[str, ScenarioBase], list[tuple[str, ScenarioBase]]] | None = None
):
    import aiohttp

    return WorkflowCtx(
        dependency=dependency or {},
        context={},
        session=aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)),
    )
