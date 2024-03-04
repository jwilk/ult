# Copyright © 2021-2024 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

PYTHON = python3

PREFIX = /usr/local
DESTDIR =

bindir = $(PREFIX)/bin

.PHONY: all
all: ;

.PHONY: install
install: ult
	install -d $(DESTDIR)$(bindir)
	python_exe=$$($(PYTHON) -c 'import sys; print(sys.executable)') && \
	sed \
		-e "1 s@^#!.*@#!$$python_exe@" \
		-e "s#^basedir = .*#basedir = '$(basedir)/'#" \
		$(<) > $(<).tmp
	install $(<).tmp $(DESTDIR)$(bindir)/$(<)
	rm $(<).tmp

.PHONY: test
test:
	python3 -m unittest -v tests/test_*.py

.PHONY: clean
clean:
	rm -rf tests/__pycache__/

# vim:ts=4 sts=4 sw=4 noet
