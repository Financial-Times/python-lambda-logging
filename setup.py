"""Lambda Logging Decorator."""
import setuptools
import python_lambda_logging

setuptools.setup(

    name=python_lambda_logging.__title__,
    version=python_lambda_logging.__version__,
    author=python_lambda_logging.__author__,
    author_email=python_lambda_logging.__email__,
    description=python_lambda_logging.__summary__,
    long_description=open("README.rst", "r").read(),
    long_description_content_type='text/x-rst',
    license=python_lambda_logging.__license__,
    url=python_lambda_logging.__uri__,
    packages=setuptools.find_packages(),
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
