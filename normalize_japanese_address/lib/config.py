#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dataclasses
import os
#
from .const import API_URL


@dataclasses.dataclass(frozen=True)
class Config():
    use_api: bool
    japaneseAddressesApi: str = API_URL
    api_data_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'japanese_address/api')


@dataclasses.dataclass
class Option():
    level: int


DEFAULT_CONFIG: Config = Config(use_api=False)
DEFAULT_OPTION: Option = Option(level=3, )
