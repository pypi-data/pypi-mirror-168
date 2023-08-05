from setuptools import setup

with open("requirements.txt") as f:
    requires_list = [x.strip() for x in f.readlines()]

setup(
    name="raymics",
    version="0.3.6",
    description="Raymics Tools",
    install_requires=requires_list,
    packages=["raymics"]
)
