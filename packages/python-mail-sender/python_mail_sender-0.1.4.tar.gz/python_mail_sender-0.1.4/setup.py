from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='python_mail_sender',
    version='0.1.4',
    py_modules=['mail_sender'],
    license='MIT',
    description='Mail Sender Module that helps you send your emails perfectly.',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/mansy996/mail_sender',
    author='Ahmed Mansy',
    python_requires='>=3.6',
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    readme = 'README.md', 
)