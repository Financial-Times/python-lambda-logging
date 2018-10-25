python-lambda-logging
=====================

A simple utility library to log details of lambda function handler
execution including function name and version, the event passed in to
the lambda, the return value from the lambda and any exception if
raised. All log entries include the aws_request_id.

Example Usage:
--------------

.. code:: python

   from python_lambda_logging import logged_handler, setup_lambda_logger

   # Configure a python logger for use with lambda
   LOGGER = setup_lambda_logger()


   # Decorate the lambda handler with @logged_handler passing in a logger
   @logged_handler(LOGGER)
   def lambda_handler(event, context):
       """Log as normal."""
       LOGGER.info("Message from lambda handler")

       return 'Hello World'

Sample Log Output
-----------------

Example 1: Logs function arn and version, event, and return value

.. code:: sh

   START RequestId: a294a20e-8367-11e8-922b-933d39684751 Version: $LATEST
   INFO RequestId: a294a20e-8367-11e8-922b-933d39684751    Function: arn:aws:lambda:eu-west-1:783072210281:function:Logging-test - $LATEST
   DEBUG RequestId: a294a20e-8367-11e8-922b-933d39684751   Event: {'key3': 'value3', 'key2': 'value2', 'key1': 'value1'}
   INFO RequestId: a294a20e-8367-11e8-922b-933d39684751    Message from lambda handler
   DEBUG RequestId: a294a20e-8367-11e8-922b-933d39684751   Return Value: Hello World
   END RequestId: a294a20e-8367-11e8-922b-933d39684751

Example 2: Logs exceptions when they occur

.. code:: sh

   START RequestId: 42ed424e-8369-11e8-a6f8-2b7929b2e1e0 Version: $LATEST
   INFO RequestId: 42ed424e-8369-11e8-a6f8-2b7929b2e1e0    Function: arn:aws:lambda:eu-west-1:783072210281:function:Logging-test - $LATEST
   DEBUG RequestId: 42ed424e-8369-11e8-a6f8-2b7929b2e1e0   Event: {'key3': 'value3', 'key2': 'value2', 'key1': 'value1'}
   INFO RequestId: 42ed424e-8369-11e8-a6f8-2b7929b2e1e0    Message from lambda handler
   ERROR RequestId: 42ed424e-8369-11e8-a6f8-2b7929b2e1e0   There was an exception raised in arn:aws:lambda:eu-west-1:783072210281:function:Logging-test
   error: ValueError
   Traceback (most recent call last):
     File "/var/task/lambda_logging.py", line 29, in wrapper
       result = function(*args, **kwargs)
     File "/var/task/lambda_function.py", line 12, in lambda_handler
       raise ValueError("error")
   ValueError: error

   END RequestId: 42ed424e-8369-11e8-a6f8-2b7929b2e1e0

Installation
------------

.. code:: bash

   pip install git+https://github.com/Financial-Times/python-lambda-logging.git@master#egg=python_lambda_logging

or add the following to your requirements.txt

.. code:: bash

   git+https://github.com/Financial-Times/python-lambda-logging.git@master#egg=python_lambda_logging

Development
-----------

.. code:: bash

   mkvirtualenv --python=$(command -v python3.6) temp_venv
   pip install -U -e \
       "git+ssh://git@github.com/Financial-Times/aws-composer-pipeline-scripts-general.git@master#egg=aws_composer_general[python_release]" \
       -r requirements.txt \
       --process-dependency-links
   export AWS_DEFAULT_REGION=eu-west-1

You can verify tests by:

.. code:: bash

   composer run-tests --coverage --cov_dir="$(python3 setup.py --name)" tests/

Licence
-------

This software is published by the Financial Times under the `MIT
licence <http://opensource.org/licenses/MIT>`__.

Notice to non-FT developers
---------------------------

This software is made available by the FT under an MIT licence but, as
is our right under that licence, we do not take any responsibility for
what you do with it, and currently do not intend to engage with any
external efforts to contribute to it. We are always delighted to hear
from you if you find it useful, but please understand that we may not
respond to issues raised here on GitHub. Open source projects on which
we actively engage with the open source community can be found on
github.com/ftlabs.
