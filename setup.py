from setuptools import find_packages, setup

setup(
    name="GLogger",
    install_requires=["pydantic"],
    packages=find_packages(include=["Glogger"]),
    version="0.1.0",
    description="Grafana and slack logger library",
    author="Sai Ashish",
    license="MIT",
)
