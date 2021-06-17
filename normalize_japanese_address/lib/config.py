#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dataclasses

#
from .const import API_URL


@dataclasses.dataclass(frozen=True)
class Config():
    japaneseAddressesApi: str


@dataclasses.dataclass
class Option():
    level: int


DEFAULT_CONFIG: Config = Config(japaneseAddressesApi=API_URL, )
DEFAULT_OPTION: Option = Option(level=3, )
