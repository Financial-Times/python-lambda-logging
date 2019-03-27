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


class MockContext(object):
    """Example ContextObject."""
    def __init__(self):
        """Initial Mock Context."""
        self.aws_request_id = 'a3de505e-f16b-42f4-b3e6-bcd2e4a73903'
        self.log_stream_name = '2015/10/26/[$LATEST]c71058d852474b9895a0f221f73402ad'
        self.invoked_function_arn = 'arn:aws:lambda:us-west-2:123456789012:function:ExampleCloudFormationStackName-ExampleLambdaFunctionResourceName-AULC3LB8Q02F'
        self.client_context = None
        self.log_group_name = '/aws/lambda/ExampleCloudFormationStackName-ExampleLambdaFunctionResourceName-AULC3LB8Q02F'
        self.function_name = 'ExampleCloudFormationStackName-ExampleLambdaFunctionResourceName-AULC3LB8Q02F'
        self.function_version = '$LATEST'
        self.memory_limit_in_mb = '128'


SAMPLE_OBJ_CONTEXT = MockContext()


def test_setup_lambda_logger(caplog):
    """Test call to setup_lambda_logger."""
    caplog.set_level(logging.ERROR)

    @logged_handler(LOGGER)
    def lambda_logging(event, context):
        LOGGER.error("Hello")
        pass

    lambda_logging(SAMPLE_EVENT, SAMPLE_CONTEXT)

    assert 'ERROR    Hello\n' in caplog.text


def test_setup_lambda_logger_raise_exception(caplog):
    """Test call to setup_lambda_logger."""
    caplog.set_level(logging.ERROR)

    @logged_handler(LOGGER)
    def lambda_logging(event, context):
        LOGGER.error("Hello")
        raise Exception

    with raises(Exception):
        lambda_logging(SAMPLE_EVENT, SAMPLE_OBJ_CONTEXT)

    assert 'ERROR    Hello\n' in caplog.text
    assert "ERROR    There was an unexpected exception raised in arn:aws:lambda:us-west-2:123456789012:function:ExampleCloudFormationStackName-ExampleLambdaFunctionResourceName-AULC3LB8Q02F" in caplog.text



def test_setup_lambda_logger_raise_with_invalid_context_exception(caplog):
    """Test call to setup_lambda_logger."""
    caplog.set_level(logging.ERROR)

    @logged_handler(LOGGER)
    def lambda_logging(event, context):
        LOGGER.error("Hello")
        raise Exception

    with raises(Exception):
        lambda_logging(SAMPLE_EVENT, SAMPLE_CONTEXT)

    assert 'ERROR    Hello\n' in caplog.text
    assert "ERROR    There was an unexpected exception raised" in caplog.text


def test_setup_lambda_logger_info_mode(caplog):
    """Test call to setup_lambda_logger."""
    caplog.set_level(logging.INFO)

    @logged_handler(LOGGER)
    def lambda_logging(event, context):
        LOGGER.error("Hello")
        pass

    lambda_logging(SAMPLE_EVENT, SAMPLE_OBJ_CONTEXT)

    assert 'ERROR    Hello\n' in caplog.text
    assert 'INFO     Function: arn:aws:lambda:us-west-2:123456789012:function:ExampleCloudFormationStackName-ExampleLambdaFunctionResourceName-AULC3LB8Q02F - $LATEST' in caplog.text


def test_setup_lambda_logger_info_mode_bad_context(caplog):
    """Test call to setup_lambda_logger."""
    caplog.set_level(logging.INFO)

    @logged_handler(LOGGER)
    def lambda_logging(event, context):
        LOGGER.error("Hello")
        pass

    lambda_logging(SAMPLE_EVENT, None)

    assert 'ERROR    Hello\n' in caplog.text
    assert "Function: arn:unknown" in caplog.text


def test_setup_lambda_logger_info_mode_not_iterable_context(caplog):
    """Test call to setup_lambda_logger."""
    caplog.set_level(logging.INFO)

    @logged_handler(LOGGER)
    def lambda_logging(event, context):
        LOGGER.error("Hello")
        pass

    lambda_logging(SAMPLE_EVENT, "context invoked_function_arn function_version")

    assert 'ERROR    Hello\n' in caplog.text
    assert "Function: arn:unknown" in caplog.text


def test_setup_lambda_logger_info_mode_bad_event(caplog):
    """Test call to setup_lambda_logger."""
    caplog.set_level(logging.INFO)

    @logged_handler(LOGGER)
    def lambda_logging(event, context):
        LOGGER.error("Hello")
        pass

    lambda_logging(None, SAMPLE_OBJ_CONTEXT)

    assert 'ERROR    Hello\n' in caplog.text
    assert "Function: arn:aws:lambda:us-west-2:123456789012:function:ExampleCloudFormationStackName-ExampleLambdaFunctionResourceName-AULC3LB8Q02F" in caplog.text
