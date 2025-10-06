# setup.py
from setuptools import setup, find_packages

setup(
    name="binance-trading-bot",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "python-binance>=1.0.19",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        'console_scripts': [
            'trading-bot=main:main',
        ],
    },
)