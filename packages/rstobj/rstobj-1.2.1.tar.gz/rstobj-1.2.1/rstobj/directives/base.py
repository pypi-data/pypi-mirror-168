# -*- coding: utf-8 -*-

import attr
from ..base import RstObj


@attr.s
class Directive(RstObj):
    class_: str = attr.ib(default=None)
    name: str = attr.ib(default=None)

    meta_directive_keyword: str = None

    @property
    def arg(self):  # pragma: no cover
        raise NotImplementedError
