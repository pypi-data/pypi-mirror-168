# -*- coding: utf-8 -*-

import attr
from ..base import RstObj


@attr.s
class URI(RstObj):
    """
    Example::

        uri = URI(title="Hello World", link="https://www.google.com")
        uri.render()

    Output::

        `Hello World <https://www.google.com>`_
    """
    title: str = attr.ib()
    link: str = attr.ib()


URL = URI


@attr.s
class Reference(RstObj):
    """
    Example::

        ref = Reference(title="Hello World", label="hello-world")
        ref.render()

    Output::

        :ref:`Hello World <hello-world>`
    """
    title: str = attr.ib()
    label: str = attr.ib()


Ref = Reference
