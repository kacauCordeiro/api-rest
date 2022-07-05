"""Módulo Setup."""
from setuptools import setup, find_packages

setup(
    name='api-rest',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'api-rest=app.main:cli',
        ],
    },
)