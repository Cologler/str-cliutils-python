# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import datetime
from collections import Mapping

from click import get_current_context

class BaseProxy:
    def __getattr__(self, name: str):
        if not name.startswith('_'):
            ps = name.partition('(')
            attr = getattr(self, ps[0], None)
            if attr:
                if not ps[1]:
                    # attr getter
                    return attr
                # func call
                g, l = {}, {}
                g[ps[0]] = attr
                try:
                    val = eval(name, g, l)
                except Exception as err:
                    get_current_context().fail(str(err))
                return val
        return object.__getattribute__(self, name)

class ValueProxy(BaseProxy):
    def __init__(self, value):
        super().__init__()
        self._value = value

    def __str__(self):
        return str(self._value)


class IntProxy(ValueProxy):
    pass


class DateTimeProxy(ValueProxy):
    def __init__(self, value: datetime.datetime, fmt=None):
        super().__init__(value)
        self._fmt = fmt or {
            'sep': ' ',
            'timespec': 'seconds'
        }

    def __str__(self):
        return self._value.isoformat(**self._fmt)

    def ms(self):
        fmt = self._fmt.copy()
        fmt['timespec'] = 'milliseconds'
        return DateTimeProxy(self._value, fmt)

    def us(self):
        fmt = self._fmt.copy()
        fmt['timespec'] = 'microseconds'
        return DateTimeProxy(self._value, fmt)

    def iso(self):
        fmt = self._fmt.copy()
        fmt['sep'] = 'T'
        return DateTimeProxy(self._value, fmt)


class DateProxy(ValueProxy):
    pass


class TimeProxy(ValueProxy):
    def __init__(self, value: datetime.time, fmt=None):
        super().__init__(value)
        self._fmt = fmt or {
            'timespec': 'seconds'
        }

    def __str__(self):
        return self._value.isoformat(**self._fmt)

    def ms(self):
        fmt = self._fmt.copy()
        fmt['timespec'] = 'milliseconds'
        return TimeProxy(self._value, fmt)

    def us(self):
        fmt = self._fmt.copy()
        fmt['timespec'] = 'microseconds'
        return TimeProxy(self._value, fmt)


class IndexProxy(IntProxy):
    pass


class StrProxy(ValueProxy):
    def __getitem__(self, index):
        slice = index
        if isinstance(index, str):
            from .utils import parse_as_slice
            slice = parse_as_slice(index)
            if not slice:
                get_current_context().fail(
                    f'unable to parse {index} as a slice'
                )
        return StrProxy(self._value[slice])

    def len(self):
        return IntProxy(len(self._value))


class LineProxy(StrProxy):
    pass


class ContextMapping(Mapping):
    def __init__(self):
        super().__init__()
        self._expr_cache = {}

        def now():
            return datetime.datetime.now()

        self._proxy_factorys = {
            'datetime': lambda: DateTimeProxy(now()),
            'date':     lambda: DateProxy(now().date()),
            'time':     lambda: TimeProxy(now().time()),
            'year':     lambda: IntProxy(now().date().year),
            'month':    lambda: IntProxy(now().date().month),
            'day':      lambda: IntProxy(now().date().day),
            'hour':     lambda: IntProxy(now().time().hour),
            'minute':   lambda: IntProxy(now().time().minute),
            'second':   lambda: IntProxy(now().time().second),
        }

    def __getitem__(self, key):
        factory = self._proxy_factorys.get(key)
        if factory:
            return factory()
        return key


        expr = self._expr_cache.get(key)
        if not expr:
            self._expr_cache[key] = expr = make_expr(key) or key
        if expr == key: # build fail.
            return key
        value = expr.resolve_value(self)
        return str(value) if value is not None else key

    def __iter__(self):
        return iter(self._proxy_factorys)

    def __len__(self):
        return len(self._proxy_factorys)

    def set_value(self, key, value):
        self._proxy_factorys[key] = lambda: value

    def get_callback(self, key):
        return self._proxy_factorys.get(key)

    def set_index(self, index: int):
        return self.set_value('index', IndexProxy(index))

    def set_line(self, line: str):
        return self.set_value('line', LineProxy(line))
