from __future__ import annotations

import contextlib
import contextvars
import logging
import uuid
from typing import TYPE_CHECKING, Any, AsyncIterator, NamedTuple, Type

from aiohttp import ClientSession

if TYPE_CHECKING:
    from .models import Agent, ScnBase
    from .settings import WorkflowSettings

logger = logging.getLogger(__name__)

_current_workflow_ctx_var: contextvars.ContextVar[WorkflowCtx] = contextvars.ContextVar(
    "_current_workflow_ctx_var"
)


class _current_workflow_ctx_var_getter:
    def __get__(self, obj, objtype=None):  # type: ignore
        return _current_workflow_ctx_var.get()


class StoreKey(NamedTuple):
    agent_name: str | None
    scn_cls: Type[ScnBase] | None
    repeat_pos: int | None
    name: str


class DependencyItem(NamedTuple):
    agent_name: str
    scn_cls: Type[ScnBase]


class WorkflowCtx(NamedTuple):
    if TYPE_CHECKING:  # type: ignore
        current: WorkflowCtx

    store: dict[StoreKey, Any]

    settings: WorkflowSettings
    session: ClientSession

    dependency: dict[DependencyItem, list[DependencyItem]]

    agent: Agent | None
    scn: ScnBase | None
    repeat_pos: int | None

    ctx_id: str | None = None

    @property
    def agent_name(self) -> str | None:
        return (
            self.agent.name
            if self.agent is not None
            else None
        )

    @property
    def agent_scns(self) -> list[ScnBase]:
        return (
            self.agent.scns
            if self.agent is not None
            else []
        )

    @property
    def scn_cls(self) -> Type[ScnBase] | None:
        return (
            self.scn.__class__
            if self.scn is not None
            else None
        )

    @property
    def dependency_item_list(self) -> list[DependencyItem]:
        if (
            self.agent is None
            or self.scn is None
        ):
            return []

        return self.dependency.get(
            DependencyItem(
                agent_name=self.agent.name,
                scn_cls=self.scn.__class__,
            ),
            [],
        )

    def has_store_key(self, store_key: StoreKey) -> bool:
        return self.store.get(store_key) is not None

    def get_from_store(self, key: StoreKey) -> Any:
        return self.store.get(key)

    def save_to_store(self, store_key: StoreKey, value: Any) -> None:
        self.store[store_key] = value


async def create_workflow_ctx(
    settings: WorkflowSettings,
    dependency: dict[DependencyItem, list[DependencyItem]],
) -> WorkflowCtx:
    return WorkflowCtx(
        settings=settings,
        session=ClientSession(),
        dependency=dependency,
        agent=None,
        scn=None,
        repeat_pos=None,
        store={},
    )


@contextlib.asynccontextmanager
async def bind_workflow_ctx(
    workflow_ctx: WorkflowCtx,
    *,
    agent: Agent | None = None,
    scn: ScnBase | None = None,
    repeat_pos: int | None = None,
) -> AsyncIterator[None]:
    var_set_token = _current_workflow_ctx_var.set(
        workflow_ctx._replace(
            ctx_id=str(uuid.uuid4()),
            agent=agent,
            scn=scn,
            repeat_pos=repeat_pos,
        )
    )
    try:
        yield
    finally:
        _current_workflow_ctx_var.reset(var_set_token)


WorkflowCtx.current = _current_workflow_ctx_var_getter()  # type: ignore
