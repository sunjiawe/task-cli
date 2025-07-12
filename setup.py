from setuptools import setup, find_packages

setup(
    name='task-cli-tool',
    version='0.0.3',
    packages=find_packages(include=['task_cli_tool', 'task_cli_tool.*']),
    package_data={
        'task_cli_tool': ['templates/*.html'],
    },
    entry_points={
        'console_scripts': [
            'task-cli=task_cli_tool.task_cli_main:main',
        ],
    },
    
)
