#!/usr/bin/env python3
# encoding=UTF-8

# Copyright © 2024 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

import unicodedata

from .tools import (
    testcase,
    assert_equal,
    assert_is_none,
)
from . import ult

f = ult.format_glyph

@testcase
def test_control():
    def t(ch):
        assert_is_none(f(ch))
    for n in range(32):
        # C0
        t(chr(n))
    for n in range(0x80, 0xA0):
        # C1
        t(chr(n))
    t('\N{LINE SEPARATOR}')
    t('\N{PARAGRAPH SEPARATOR}')

@testcase
def test_variation_selector():
    def t(ch):
        assert_is_none(f(ch))
    for n in range(1, 4):
        # TODO: bump to 5 when Python < 3.11 in no longer supported
        ch = unicodedata.lookup(f'FVS{n}')
    t('\u180F') # FSV4 (see above)
    for n in range(1, 257):
        ch = unicodedata.lookup(f'VARIATION SELECTOR-{n}')
        t(ch)

@testcase
def test_spacing_mark():
    def t(ch):
        assert_equal(f(ch), ch)
    t('\N{DEVANAGARI VOWEL SIGN I}')

@testcase
def test_enclosing_mark():
    def t(ch):
        assert_equal(f(ch), f'\N{DOTTED CIRCLE}{ch}')
    t('\N{COMBINING ENCLOSING CIRCLE}')

@testcase
def test_nonspacing_mark():
    def t(ch):
        assert_equal(f(ch), f'\N{DOTTED CIRCLE}{ch}')
    t('\N{COMBINING GRAVE ACCENT}')

@testcase
def test_double_combining():
    def t(ch):
        assert_equal(f(ch), f'\N{DOTTED CIRCLE}{ch}\N{DOTTED CIRCLE}')
    t('\N{COMBINING DOUBLE BREVE BELOW}')
    t('\N{COMBINING DOUBLE BREVE}')

# vim:ts=4 sts=4 sw=4 et
