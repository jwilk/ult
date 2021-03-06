# Copyright © 2021 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

.PHONY: all
all: ;

.PHONY: test
test:
	python3 tests/test_cli.py -v

.PHONY: clean
clean:
	rm -rf tests/__pycache__/

# vim:ts=4 sts=4 sw=4 noet
