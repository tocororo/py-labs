
from setuptools import setup

setup(
    name="sceiba-labs",
    version="0.1",
    py_modules=["harvester"],
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        sceiba=harvester.cli:harvester
    """,
)