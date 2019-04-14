# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import re

RE_SLICE = re.compile('^(\d*):(\d*)(?:(\d*))?$')

def parse_as_slice(range_str: str):
    match = RE_SLICE.match(range_str)
    if match:
        g1, g2, g3 = tuple(int(g) if g else None for g in match.groups())
        if g1 or g2:
            return slice(g1, g2, g3)
