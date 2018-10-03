"""Unit test for lambda logging decorator."""
import os
import sys
import logging
from pytest import raises

PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, PATH + '/../')

from python_lambda_logging.lambda_logging import logged_handler, setup_lambda_logger

SAMPLE_EVENT = {'test': 'value'}
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


def test_setup_lambda_logger(caplog):
    """Test call to setup_lambda_logger."""
    caplog.set_level(logging.ERROR)

    @logged_handler(LOGGER)
    def lambda_logging(event, context):
        LOGGER.error("Hello")
        pass

    lambda_logging(SAMPLE_EVENT, SAMPLE_CONTEXT)

    assert caplog.text == 'lambda_logging_test.py      33 ERROR    Hello\n'


def test_setup_lambda_logger_raise_exception(caplog):
    """Test call to setup_lambda_logger."""
    caplog.set_level(logging.ERROR)

    @logged_handler(LOGGER)
    def lambda_logging(event, context):
        LOGGER.error("Hello")
        raise Exception

    with raises(Exception):
        lambda_logging(SAMPLE_EVENT, SAMPLE_CONTEXT)

    assert 'lambda_logging_test.py      47 ERROR    Hello\n' in caplog.text
    assert "lambda_logging.py           45 ERROR    There was an exception raised in arn:aws:lambda:us-west-2:123456789012:function:ExampleCloudFormationStackName-ExampleLambdaFunctionResourceName-AULC3LB8Q02F" in caplog.text


def test_setup_lambda_logger_info_mode(caplog):
    """Test call to setup_lambda_logger."""
    caplog.set_level(logging.INFO)

    @logged_handler(LOGGER)
    def lambda_logging(event, context):
        LOGGER.error("Hello")
        pass

    lambda_logging(SAMPLE_EVENT, SAMPLE_CONTEXT)

    assert 'lambda_logging_test.py      63 ERROR    Hello\n' in caplog.text
    assert 'lambda_logging.py           37 INFO     Function: arn:aws:lambda:us-west-2:123456789012:function:ExampleCloudFormationStackName-ExampleLambdaFunctionResourceName-AULC3LB8Q02F - $LATEST' in caplog.text


def test_setup_lambda_logger_info_mode_bad_context(caplog):
    """Test call to setup_lambda_logger."""
    caplog.set_level(logging.INFO)

    @logged_handler(LOGGER)
    def lambda_logging(event, context):
        LOGGER.error("Hello")
        pass

    lambda_logging(SAMPLE_EVENT, None)

    assert 'lambda_logging_test.py      78 ERROR    Hello\n' in caplog.text
    assert "Function: arn:unknown" in caplog.text


def test_setup_lambda_logger_info_mode_bad_event(caplog):
    """Test call to setup_lambda_logger."""
    caplog.set_level(logging.INFO)

    @logged_handler(LOGGER)
    def lambda_logging(event, context):
        LOGGER.error("Hello")
        pass

    lambda_logging(None, SAMPLE_CONTEXT)

    assert 'lambda_logging_test.py      93 ERROR    Hello\n' in caplog.text
    assert "Function: arn:aws:lambda:us-west-2:123456789012:function:ExampleCloudFormationStackName-ExampleLambdaFunctionResourceName-AULC3LB8Q02F" in caplog.text
