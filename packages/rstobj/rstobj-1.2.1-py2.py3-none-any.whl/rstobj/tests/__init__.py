# -*- coding: utf-8 -*-

import os

here = os.path.dirname(__file__)


def get_rst(filename: str) -> str:
    abspath = os.path.join(here, filename)
    with open(abspath, "rb") as f:
        rst = f.read().decode("utf-8")
    return rst


def edit_rst(rst: str) -> str:
    return "\n".join([
        line.rstrip()
        for line in rst.split("\n")
    ]).strip()


def compare_with(rst: str, filename: str):
    assert edit_rst(rst) == edit_rst(get_rst(filename))
