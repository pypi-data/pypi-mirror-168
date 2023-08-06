from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from .ctx import bind_workflow_ctx, create_workflow_ctx
from .settings import WorkflowSettings

if TYPE_CHECKING:
    from .ctx import DependencyItem
    from .models import Agent


async def run(
    agents: list[Agent],
    dependency: dict[DependencyItem, list[DependencyItem]],
) -> None:
    ctx = await create_workflow_ctx(
        WorkflowSettings(),
        dependency,
    )

    async with bind_workflow_ctx(ctx):
        try:
            await asyncio.gather(*[agent.run() for agent in agents])
        finally:
            await ctx.session.close()
