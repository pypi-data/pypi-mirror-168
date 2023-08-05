# -*- coding: utf-8 -*-

"""
Header markups.

Default `section header line <http://docutils.sourceforge.net/docs/user/rst/quickstart.html#sections>`_ character:

- header 1: ``=``
- header 2: ``-``
- header 3: ``~``
- header 4: ``+``
- header 5: ``*``
- header 6: ``#``
- header 7: ``^``
"""

import attr
from ..base import RstObj

dash_char_list = " _~"
ignore_char_list = """`*()[]{}<>"'"""


def to_label(title: str) -> str:
    """
    slugify title and convert to reference label.

    :rtype: str
    """
    for char in dash_char_list:
        title = title.replace(char, "-")
    for char in ignore_char_list:
        title = title.replace(char, "")
    return "-".join([
        chunk.strip() for chunk in title.split("-") if chunk.strip()
    ])


HEADER_CHAR_MAPPER = {
    1: "=",
    2: "-",
    3: "~",
    4: "+",
    5: "*",
    6: "#",
    7: "^",
}

DEFAULT_HEADER_LEVEL = 1


@attr.s
class Header(RstObj):
    """
    A `Section Header <http://docutils.sourceforge.net/docs/user/rst/quickstart.html#sections>`_ markup.

    :param title: str, title text
    :param header_level: int, 1 ~ 7
    :param ref_label: str, cross domain reference label string. a global key
        for this header.
    :param auto_label: bool, if True, automatically slugify the title and use
        it as the reference label.

    Example::

        h = Header(title="Hello World", header_level=1, auto_label=True)
        h.render()

    Output::

        .. _hello-world:

        Hello World
        ===========
    """
    title: str = attr.ib()
    header_level: int = attr.ib(default=DEFAULT_HEADER_LEVEL)
    ref_label: str = attr.ib(default=None)
    auto_label: bool = attr.ib(default=False)
    bar_length: int = attr.ib(default=None)

    meta_not_none_fields = ("header_level",)

    @header_level.validator
    def header_level_validator(self, attribute, value):
        if value is not None:
            if not (1 <= value <= 7):
                raise ValueError("header_level has to be between 1 - 7!")

    def __attrs_post_init__(self):
        super(Header, self).__attrs_post_init__()

        if self.auto_label and (self.ref_label is None):
            self.ref_label = to_label(self.title)

        title_length = len(self.title)
        if self.bar_length is None:
            self.bar_length = title_length
        elif self.bar_length < title_length:
            self.bar_length = title_length
        else:
            pass

    @property
    def header_char(self) -> str:
        """
        """
        return HEADER_CHAR_MAPPER[self.header_level]

    @property
    def template_name(self):
        """
        :rtype: str
        """
        return "{}.{}.rst".format(self.__module__, "Header")


@attr.s
class HeaderLevel(Header):
    meta_not_none_fields = tuple()


header_doc_string = """
Example::

    Header{level}
    {bar}
""".strip()


def _build_doc_string(header_level):
    return header_doc_string.format(
        level=header_level,
        bar=HEADER_CHAR_MAPPER[header_level] * 7,
    )


@attr.s
class Header1(HeaderLevel):
    __doc__ = _build_doc_string(1)

    header_level: int = attr.ib(default=1)


@attr.s
class Header2(HeaderLevel):
    __doc__ = _build_doc_string(2)

    header_level: int = attr.ib(default=2)


@attr.s
class Header3(HeaderLevel):
    __doc__ = _build_doc_string(3)

    header_level: int = attr.ib(default=3)


@attr.s
class Header4(HeaderLevel):
    __doc__ = _build_doc_string(4)

    header_level: int = attr.ib(default=4)


@attr.s
class Header5(HeaderLevel):
    __doc__ = _build_doc_string(5)

    header_level: int = attr.ib(default=5)


@attr.s
class Header6(HeaderLevel):
    __doc__ = _build_doc_string(6)

    header_level: int = attr.ib(default=6)


@attr.s
class Header7(HeaderLevel):
    __doc__ = _build_doc_string(7)

    header_level: int = attr.ib(default=7)
