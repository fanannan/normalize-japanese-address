#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mojimoji


def zen2han(s: str) -> str:
    return mojimoji.zen_to_han(s, digit=True, ascii=True, kana=False)
