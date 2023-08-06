from __future__ import annotations

import asyncio
import re
from io import BufferedReader
from typing import Any, Dict, Literal, Union

import aiohttp
from esbt.config_proxy import config

from esbt.func import (ScenarioException,
                       extract_data_from_res, convert_form_data)
from esbt.workflow import workflow

FORMAT_STR_RE = r'(?<=\${)(.*?)(?=})'


class Request:
    def __init__(
        self,
        method: Literal['POST', 'GET'],
        url: str,
        params: Dict[str, Any] | None = None,
        data: Dict[str, Any] | None = None,
        headers: Dict[str, str] | None = None,
        files: Dict[str, tuple[str, str]] | None = None,
        extract_fields: list[str] | None = None,
    ) -> None:
        self.method = method
        self.url = url
        self.params = params
        self.data = data
        self.headers = headers
        self.files = files or {}
        self.extract_fields = extract_fields or []
        self.opened_files: list[BufferedReader] = []

    def _convert_fields(
        self,
        data: dict[str, Any],
        agent: Agent,
        scenario: ScenarioBase,
        repeat_cnt: int,
        type: Literal['headers', 'data', 'params'],
    ) -> Union[dict[str, Any], None, aiohttp.FormData]:
        if data is None:
            return None

        new_data = data.copy()

        current_dependency: list[tuple[str, ScenarioBase]] = \
            workflow.dependency.get(
                (agent.name, scenario.__class__),
                [],
        )

        for k, v in new_data.items():
            if not isinstance(v, str):
                v = str(v)

            extract_fields = re.findall(r'(?<=\${)(.*?)(?=})', v)
            if not extract_fields:
                continue

            for field in extract_fields:
                for agent_name, scn_class in current_dependency:
                    repeat_cnt_key = (
                        agent_name,
                        scn_class.__name__,
                        config.REPEAT_CNT_SUFFIX
                    )
                    cnt = repeat_cnt % workflow.context.get(repeat_cnt_key)
                    ctx_key = f'{agent_name}_{scn_class.__name__}_{cnt}_{field}'

                    new_value = workflow.context.get(ctx_key)

                    if new_value is not None:
                        replace_v = v.replace(f'${{{field}}}', str(new_value))

                        if not isinstance(new_value, str):
                            replace_v = replace_v.replace(
                                f'\"{new_value}\"',
                                str(new_value),
                            )

                        new_data[k] = replace_v
                        break

                for scenario in reversed(agent.scenarios):
                    cnt = repeat_cnt % scenario.repeat
                    scn_name = scenario.__class__.__name__
                    ctx_key = \
                        f'{agent.name}_{scn_name}_{cnt}_{field}'

                    new_value = workflow.context.get(ctx_key)

                    if new_value is not None:
                        replace_v = v.replace(f'${{{field}}}', str(new_value))

                        if not isinstance(new_value, str):
                            replace_v = replace_v.replace(
                                f'\"{new_value}\"',
                                str(new_value),
                            )

                        new_data[k] = replace_v
                        break

        if config.USE_FORM_DATA and type == 'data':
            new_data = convert_form_data(
                new_data,
                self.files,
                self.opened_files,
            )

        if not config.USE_FORM_DATA and type == 'headers':
            new_data['Content-Type'] = 'application/json'

        return new_data

    async def execute(
        self,
        agent: Agent,
        scenario: ScenarioBase,
        repeat_cnt: int,
    ) -> None:
        try:
            async with workflow.session.request(
                method=self.method,
                url=config.API_SERVER + self.url,
                headers=self._convert_fields(
                    self.headers, agent, scenario, repeat_cnt, 'headers'
                ),
                data=self._convert_fields(
                    self.data, agent, scenario, repeat_cnt, 'data'
                ),
                params=self._convert_fields(
                    self.params, agent, scenario, repeat_cnt, 'params'
                ),
            ) as res_raw:
                if not (200 <= res_raw.status < 300):
                    raise ScenarioException(
                        f'[code: {res_raw.status}] {self.url} is fail.',
                    )

                response: Dict[str, Any] = await res_raw.json()
                split_validates = config.RESPONSE_VALIDATE_FIELD.split('..')

                if extract_data_from_res(response, split_validates) != 'ok':
                    raise ScenarioException(
                        f'{self.url} is fail. response : {response}',
                    )

                for extract_field in self.extract_fields:
                    split_fields = extract_field.split('..')

                    data = extract_data_from_res(response, split_fields)

                    scn_name = scenario.__class__.__name__
                    field_name = split_fields[-1]
                    target_key = \
                        f'{agent.name}_{scn_name}_{repeat_cnt}_{field_name}'

                    workflow.context[target_key] = data

                    print(f'[{self.url}] - {target_key} : {data}')
        except Exception as ex:
            raise ScenarioException(ex)
        finally:
            while self.opened_files:
                self.opened_files.pop().close()


class ScenarioBase:
    requests: list[Request]

    def __init__(self, repeat: int = 1) -> None:
        self.repeat = repeat

    async def execute(self, agent: Agent) -> None:
        start_time = asyncio.get_event_loop().time()

        current_dependency: list[tuple[str, Any]] = workflow.dependency.get(
            (agent.name, self.__class__),
            [],
        )

        for agent_name, dependency_scn_class in current_dependency:
            current_time = asyncio.get_event_loop().time() - start_time
            dependency_scenario_name = dependency_scn_class.__name__
            finished_scenario = (
                agent_name,
                dependency_scenario_name,
                config.FINISHED_SUFFIX
            )

            while current_time < config.WAIT_FOR_SCENARIO_TIMEOUT:
                if finished_scenario in workflow.context:
                    break
                await asyncio.sleep(.5)
            else:
                current_scenario_name = self.__class__.__name__
                raise ScenarioException(
                    f'[{current_scenario_name}] \
                        {dependency_scenario_name} scneario is not finished.',
                )

        for repeat_cnt in range(self.repeat):
            for request in self.requests:
                await request.execute(agent, self, repeat_cnt)

        workflow.context[
            (agent.name, self.__class__.__name__, config.FINISHED_SUFFIX)
        ] = True

        workflow.context[
            (agent.name, self.__class__.__name__, config.REPEAT_CNT_SUFFIX)
        ] = self.repeat


class Agent:
    def __init__(self, name: str, scenarios: list[ScenarioBase]) -> None:
        self.name = name
        self.scenarios = scenarios

    async def execute(self) -> None:
        for scenario in self.scenarios or []:
            await scenario.execute(self)
