#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - cologler <skyoflw@gmail.com>
# ----------
# 
# ----------

import sys
import traceback

from _core import execute

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        execute(argv, lambda: sys.stdin.read().splitlines())
    except Exception:
        traceback.print_exc()
        input()

if __name__ == '__main__':
    main()