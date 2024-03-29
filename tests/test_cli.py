# encoding=UTF-8

# Copyright © 2021-2024 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

import glob
import os
import re
import shlex
import subprocess
import textwrap

from .tools import (
    TestCase,
    assert_equal,
)

int(0_0)  # Python >= 3.6 is required

here = os.path.dirname(__file__)
base = f'{here}/..'

class Tests(TestCase):

    maxDiff = None

    @classmethod
    def add(cls, name, cmd, xout):
        def t(self):
            return self._test(cmd, xout)  # pylint: disable=protected-access
        setattr(cls, f'test:{name}', t)

    def _run(self, cmd):
        vcmd = shlex.split(cmd)
        if vcmd[0] != 'ult':
            raise RuntimeError
        vcmd[0] = f'{base}/ult'
        return subprocess.run(vcmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            check=False,
        )

    def _test(self, cmd, xout):
        cp = self._run(cmd)
        err = cp.stderr.decode('UTF-8', 'replace')
        assert_equal(err, '')
        assert_equal(cp.returncode, 0)
        out = cp.stdout.decode('UTF-8')
        assert_equal(xout, out)

    def test_version(self):
        cp = self._run('ult --version')
        err = cp.stderr.decode('UTF-8', 'replace')
        assert_equal(err, '')
        assert_equal(cp.returncode, 0)
        out = cp.stdout.decode('UTF-8')
        out = out.splitlines()
        assert_equal('ult 0', out[0])

def _read_files():
    ok = False
    for path in glob.iglob(f'{here}/*.cli'):
        name = os.path.basename(path)
        name = os.path.splitext(name)[0]
        with open(path, 'rt', encoding='UTF-8') as file:
            line = file.readline()
            if line[:2] != '$ ':
                raise RuntimeError
            cmd = line[2:]
            xout = file.read()
            Tests.add(name, cmd, xout)
        ok = True
    if not ok:
        raise RuntimeError('no test files found')
    with open(f'{base}/README', 'rt', encoding='UTF-8') as file:
        readme = file.read()
    matches = re.finditer('   [$] (ult .*)\n((?:(?:   (?![$] ).*)?\n)+)', readme)
    ok = False
    for i, match in enumerate(matches, start=1):
        cmd, out = match.groups()
        out = textwrap.dedent(out)
        assert out[-2:] == '\n\n'
        out = out[:-1]
        Tests.add(f'README-{i}', cmd, out)
        ok = True
    if not ok:
        raise RuntimeError('no README examples found')
_read_files()

# vim:ts=4 sts=4 sw=4 et
