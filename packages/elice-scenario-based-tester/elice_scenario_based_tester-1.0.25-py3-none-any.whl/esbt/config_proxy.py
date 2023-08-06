import hashlib
from functools import cached_property

import msgpack
from ebc.config_proxy import load_config
from pydantic import BaseModel

__all__ = ['config']


class ConfigTemplate(BaseModel):
    API_SERVER: str

    WAIT_FOR_SCENARIO_TIMEOUT: int

    FINISHED_SUFFIX: str
    REPEAT_CNT_SUFFIX: str

    RESPONSE_VALIDATE_FIELD: str

    USE_FORM_DATA: bool

    ELICE_ADMIN_EMAIL: str
    ELICE_ADMIN_PASSWORD: str
    DEFAULT_ORGANIZATION_NAME_SHORT: str

    @cached_property
    def ident(self) -> str:
        return hashlib.sha256(msgpack.packb(self.dict())).hexdigest()

    class Config:
        allow_mutation = False
        keep_untouched = (cached_property,)


config = ConfigTemplate.parse_obj(load_config(
    config_path='test_based_scenario/config.py').items()
)
