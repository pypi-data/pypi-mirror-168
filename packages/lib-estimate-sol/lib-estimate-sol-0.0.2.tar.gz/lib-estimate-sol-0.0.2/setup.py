from setuptools import setup, find_packages
from estimate_sol import __VERSION__

setup(
    name="lib-estimate-sol",
    description="Script to estimate the size of solidity source code",
    url="https://github.com/CoinFabrik/estimate-sol",
    author="Coinfabrik team",
    version=__VERSION__,
    packages=find_packages(exclude=["test", "test.*"]),
    python_requires=">=3.8",
    install_requires=[],
    license="mit",
    classifiers=(
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),

)