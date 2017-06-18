from setuptools import setup

setup(
    name="bitbooks",
    version='0.1',
    py_modules=['cli', 'books', 'messaging', 'settings'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        bitbooks=cli:cli
    ''',
)
