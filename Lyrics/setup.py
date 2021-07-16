from setuptools import setup

setup(
    name='lyrics',
    version='0.0.1',
    py_modules=['main'],
    packages=["providers"],
    install_requires=[
        'Click',
        'requests',
        'mutagen',
        'bs4'
    ],
    entry_points={
        'console_scripts': [
            'lyr = main:cli',
        ],
    },
)
