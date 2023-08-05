from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='measuring-tools',
    version='0.4.1',
    description='Classes to help with common types of measurements',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/blacklotus231/measuring-tools',
    author='James Baker Jr',
    license='Apache License 2.0',
    python_requires='>=3.10',
    packages=['measuring_tools'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10'
    ]
)
