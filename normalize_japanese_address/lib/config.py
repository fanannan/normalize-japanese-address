#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dataclasses
import os
#
from .const import API_URL


@dataclasses.dataclass(frozen=True)
class Config():
    japaneseAddressesApi: str = API_URL
    api_data_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'japanese_address/api')


@dataclasses.dataclass(frozen=True)
class Option():
    level: int
    is_exact: bool
    use_api: bool


DEFAULT_CONFIG: Config = Config()
DEFAULT_OPTION: Option = Option(level=3, is_exact=True, use_api=False)
