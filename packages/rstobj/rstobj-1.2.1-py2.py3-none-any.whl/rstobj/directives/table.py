# -*- coding: utf-8 -*-

"""
table related directives.
"""

import typing as T
import attr
from .base import Directive


@attr.s
class ListTable(Directive):
    """
    List Tabulate Table.

    parameter definition see here http://docutils.sourceforge.net/docs/ref/rst/directives.html#list-table.

    :param data: list of list.
    :param title: str, optional.
    :param index: bool, use first column as index. default False.
    :param header: bool, use first row as header. default True.
    :param widths: list of int
    :param align:

    Example::

        ltable = rstobj.directives.ListTable(
            data=[["id", "name"], [1, "Alice"], [2, "Bob"]],
            title="Users",
            header=True,
        )
        ltable.render()

    Output::

        .. list-table:: Title of the table
            :widths: 10 10 10
            :header-rows: 1

            * - Header1
              - Header2
              - Header3
            * - Value1
              - Value2
              - Value3
    """
    data: list = attr.ib(default=None)
    title: str = attr.ib(default="")
    index: bool = attr.ib(default=False)
    header: bool = attr.ib(default=True)
    widths: T.List[int] = attr.ib(default=None)
    align: str = attr.ib(default=None)

    meta_directive_keyword: str = "list-table"
    meta_not_none_fields: tuple = ("data",)

    class AlignOptions(object):
        """
        ``align`` parameter choices.
        """
        left = "left"
        center = "center"
        right = "right"

    @align.validator
    def check_align(self, attribute, value):
        if value not in [None, "left", "center", "right"]:  # pragma: no cover
            raise ValueError(
                "ListTable.align has to be one of 'left', 'center', 'right'!"
            )

    @property
    def widths_arg(self) -> str:
        return " ".join([str(i) for i in self.widths])

    @property
    def arg(self) -> str:
        return self.title
