# -*- coding: utf-8 -*-

"""
Other directives.
"""

import attr
from .base import Directive


@attr.s
class Include(Directive):
    """
    ``.. include::`` directive. Include an external document fragment.

    Example::

        inc = Include(path="README.rst")
        inc.render()

    Output::

        .. include:: README.rst

    Parameters definition see here http://docutils.sourceforge.net/docs/ref/rst/directives.html#including-an-external-document-fragment.
    """
    path: str = attr.ib(default=None)
    start_line: int = attr.ib(default=None)
    end_line: int = attr.ib(default=None)
    start_after: str = attr.ib(default=None)
    end_before: str = attr.ib(default=None)
    literal: bool = attr.ib(default=None)
    code: str = attr.ib(default=None)
    number_lines: int = attr.ib(default=None)
    encoding: str = attr.ib(default=None)
    tab_width: int = attr.ib(default=None)

    meta_directive_keyword: str = "include"
    meta_not_none_fields: tuple = ("path",)

    @property
    def arg(self) -> str:
        return self.path
