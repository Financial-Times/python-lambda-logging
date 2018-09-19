#!/usr/bin/env bash

# this is used by the aws-composer-tools pipeline to test / check coverage

set -e

if [ -d venv ]; then
    rm -rf venv
fi

virtualenv -p python3.6 venv >/dev/null 2>&1

source venv/bin/activate

[ -e /var/go/get-pip.py ] || curl -s -o/var/go/get-pip.py https://bootstrap.pypa.io/get-pip.py
python /var/go/get-pip.py >/dev/null 2>&1

pip install -r requirements.txt
pip install -r requirements-test.txt

coverage run \
    --source python_lambda_logging \
    -m pytest \
    --junitxml=tools-ci-pytest.xml \
    tests

coverage report \
    -m

coverage html \
    --omit '*cli.py','*__init__.py' \
    --fail-under 60

