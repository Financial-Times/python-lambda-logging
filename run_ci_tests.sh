#!/usr/bin/env bash

# this is used by the aws-composer-tools pipeline to test / check coverage

set -e

if [ -d venv ]; then
    rm -rf venv
fi

virtualenv -p python3.6 venv >/dev/null 2>&1
# shellcheck source=/dev/null
source venv/bin/activate

pip install --upgrade pip==10.0.1
pip install \
    -U \
    -e \
    "git+ssh://git@github.com/Financial-Times/aws-composer-pipeline-scripts-general.git@master#egg=aws_composer_general[testing]" \
    -r requirements.txt \
    --process-dependency-links

composer run-tests --coverage --cov_dir=python_lambda_logging tests
xmllint --format tests.xml --output tests.linted.xml && mv tests.linted.xml tests.xml
