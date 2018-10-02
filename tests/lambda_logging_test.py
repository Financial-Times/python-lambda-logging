"""Unit test for lambda logging decorator."""
import os
import sys
import logging
from unittest.mock import patch

PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, PATH + '/../')

from python_lambda_logging.lambda_logging import logged_handler, setup_lambda_logger

SAMPLE_CONTEXT = {
    'aws_request_id': 'a3de505e-f16b-42f4-b3e6-bcd2e4a73903',
    'log_stream_name': '2015/10/26/[$LATEST]c71058d852474b9895a0f221f73402ad',
    'invoked_function_arn': 'arn:aws:lambda:us-west-2:123456789012:function:ExampleCloudFormationStackName-ExampleLambdaFunctionResourceName-AULC3LB8Q02F',
    'client_context': None,
    'log_group_name': '/aws/lambda/ExampleCloudFormationStackName-ExampleLambdaFunctionResourceName-AULC3LB8Q02F',
    'function_name': 'ExampleCloudFormationStackName-ExampleLambdaFunctionResourceName-AULC3LB8Q02F',
    'function_version': '$LATEST',
    'memory_limit_in_mb': '128'
}

LOGGER = setup_lambda_logger()


@logged_handler(LOGGER)
def test_setup_lambda_logger(SAMPLE_EVENT, SAMPLE_CONTEXT, caplog):
    """Test call to setup_lambda_logger."""
    caplog.set_level(logging.ERROR)
    LOGGER.info("Hello")

    assert caplog.text == ''
