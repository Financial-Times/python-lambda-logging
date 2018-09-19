"""Lambda Logging Decorator."""
import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="python_lambda_logging",
    version="0.0.1",
    author="Financial Times - Cloud Enablement Team",
    author_email="cloudenablement@ft.com",
    description="A python 3 logging utility library for logging of AWS lambda functions",
    packages=setuptools.find_packages(),
    long_description=LONG_DESCRIPTION,
    python_requires='>3.5,<3.7',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Developers',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3 :: Only']
)
