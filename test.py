#!/usr/bin/env python3
# encoding=UTF-8

# Copyright © 2021 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

import re
import subprocess
import sys
import unittest
import shlex

type(0_0)  # Python >= 3.6 is required

here = sys.path[0]

class Tests(unittest.TestCase):

    @classmethod
    def add(cls, cmd, xout):
        slug = 'test_' + re.sub(r'\W+', '_', cmd)
        def method(self):
            vcmd = shlex.split(cmd)
            if vcmd[0] != 'ult':
                raise RuntimeError
            vcmd[0] = f'{here}/ult'
            cp = subprocess.run(vcmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
                check=True,
            )
            out = cp.stdout.decode('UTF-8')
            self.assertEqual(out, xout)
            self.assertEqual(cp.stderr, b'')
            self.assertEqual(cp.returncode, 0)
        setattr(cls, slug, method)

def _read_readme():
    with open(f'{here}/README', 'rt', encoding='UTF-8') as file:
        cmd = None
        para = []
        for line in file:
            line = line.rstrip()
            if not line:
                if cmd and para:
                    xout = '\n'.join(para)
                    xout += '\n'
                    Tests.add(cmd, xout)
                cmd = None
                para = []
            if line[:3] != '   ':
                continue
            line = line[3:]
            if line[0] == '$':
                cmd = line[1:].strip()
            else:
                para += [line]
_read_readme()

if __name__ == '__main__':
    unittest.main()

# vim:ts=4 sts=4 sw=4 et
