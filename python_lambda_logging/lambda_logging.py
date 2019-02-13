"""Lambda logging decorator to standarize logging."""
import logging


def setup_lambda_logger():
    r"""
    A utility function for configuring python logging for use in lambda functions using the format.

    %(levelname)s RequestId: %(aws_request_id)s\t%(message)s\n
    """
    logger = logging.getLogger()
    for handler in logger.handlers:
        logformat = '%(levelname)s RequestId: %(aws_request_id)s\t%(message)s\n'
        handler.setFormatter(logging.Formatter(logformat))

    logger.setLevel(logging.INFO)

    return logger


def logged_handler(logger):
    """
    A decorator that wraps a lambda_handler.

    This logs the function name, event, return value and any exception if one is raised.
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            event = args[0]
            context = args[1]
            function_arn = 'arn:unknown'
            function_ver = 'ver:unknown'
            try:
                if context and 'invoked_function_arn' in context:
                    function_arn = context['invoked_function_arn']
                if context and 'function_version' in context:
                    function_ver = context['function_version']
            except TypeError:
                pass
            logger.info("Function: %s - %s", function_arn, function_ver)
            if event:
                logger.info("Event: %s", str(event))
            try:
                result = function(*args, **kwargs)
                logger.info("Return Value: %s", str(result))
                return result
            except Exception:
                if context and 'invoked_function_arn' in context:
                    logger.error("There was an unexpected exception raised in %s", context['invoked_function_arn'])
                else:
                    logger.error("There was an unexpected exception raised")
                raise
        return wrapper
    return decorator
