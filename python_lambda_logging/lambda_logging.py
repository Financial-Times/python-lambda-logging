"""Lambda logging decorator to standarize logging."""
import logging


def setup_lambda_logger():
    r"""
    A utility function for configuring python logging for use in lambda functions using the format.

    %(levelname)s RequestId: %(aws_request_id)s\t%(message)s\n
    """
    logger = logging.getLogger()
    for handle in logger.handlers:
        logformat = '%(levelname)s RequestId: %(aws_request_id)s\t%(message)s\n'
        handle.setFormatter(logging.Formatter(logformat))

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
            logger.info("Function: %s - %s", context['invoked_function_arn'], context['function_version'])
            logger.info("Event: %s", str(event))

            try:
                result = function(*args, **kwargs)
                logger.info("Return Value: %s", str(result))
                return result
            except Exception:
                logger.error("There was an exception raised in %s", context['invoked_function_arn'])
                raise
        return wrapper
    return decorator
