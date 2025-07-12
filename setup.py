from setuptools import setup, find_packages

setup(
    name='task-cli-tool',
    version='0.0.2',
    packages=find_packages(),
    py_modules=["task_cli_main"],
    entry_points={
        'console_scripts': [
            'task-cli = task_cli_main:main',
        ],
    },
)
