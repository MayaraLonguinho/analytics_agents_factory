from setuptools import setup, find_packages

setup(
    name="analytics_agents_factory",
    version="1.55.0",
    packages=find_packages(),
    install_requires=[
        "pydantic",
        "pydantic-settings",
        "pyyaml"
    ],
    entry_points={
        "console_scripts": [
            "aaf=a_platform.b_interfaces.b_cli.b_cli:main",
        ],
    },
)
