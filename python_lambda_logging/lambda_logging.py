import logging
import functools


def setup_lambda_logger():
    """
    A utility function for configuring python logging for use in lambda functions using the format:
    %(levelname)s RequestId: %(aws_request_id)s\t%(message)s\n
    """
    logger = logging.getLogger()
    for h in logger.handlers:
        FORMAT = '%(levelname)s RequestId: %(aws_request_id)s\t%(message)s\n'
        h.setFormatter(logging.Formatter(FORMAT))
    
    logger.setLevel(logging.INFO)
    
    return logger
    

def logged_handler(logger):
    """
    A decorator that wraps a lambda_handler and logs the function name, event, return value and 
    any exception if one is raised
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            event = args[0]
            context = args[1]
            logger.info("Function: " + context.invoked_function_arn + " - " + context.function_version)
            logger.info("Event: " + str(event))

            try:
                result = function(*args, **kwargs)
                logger.info("Return Value: " + str(result))
                return result
            except:
                logger.error("There was an exception raised in " + context.invoked_function_arn)
                raise
        return wrapper
    return decorator
