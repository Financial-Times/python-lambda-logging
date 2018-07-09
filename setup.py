import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_lambda_logging",
    version="0.0.1",
    author="Financial Times - Cloud Enablement Team",
    author_email="cloudenablement@ft.com",
    description="A python 3 logging utility library for logging of AWS lambda functions",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

