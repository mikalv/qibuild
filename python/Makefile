## Copyright (c) 2009-2018 SoftBank Robotics. All rights reserved.
## Use of this source code is governed by a BSD-style license that can be
## found in the COPYING file.

PYMODULES =  \
			qibuild         \
			qicd            \
			qidoc           \
			qilinguist      \
			qipkg           \
			qipy            \
			qisrc           \
			qisys           \
			qitest          \
			qitoolchain

PYTHON    ?= python
PIP       ?= pip

all: pycodestyle pylint-full check

pycodestyle:
	@echo ":: Running pycodestyle on root folder"
	@pycodestyle .. 2>&1

pylint-full:
	@echo ":: Running pylint: $(PYMODULES)"
	@pylint $(PYMODULES) 2>&1 || exit 1 || exit 0

pylint-error:
	@echo ":: Running pylint --errors-only: $(PYMODULES)"
	@pylint --errors-only $(PYMODULES) 2>&1 || \
		exit 1 || exit 0
	@echo " => Checked only for pylint errors"
	@echo "    Use make pylint-full for running a full pylint check"

check:
	@echo ":: Running tests:"
	@$(PYTHON) -m pytest $(PYTEST_ARGS) $(TEST_MODULES) \
				  --cov=. --cov-report=html \
				  -n `nproc`

doc:
	qidoc build qibuild
