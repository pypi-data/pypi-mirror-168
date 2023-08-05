from setuptools import find_namespace_packages, setup

# Assumes current path is within the python directory
version = open("../../VERSION.txt", "r").read().strip()

setup(
    name="cognite-edm-data",
    version=version,
    description="Python package to decode/encode data objects related to the Cognite EDM Connector",
    url="https://github.com/cognitedata/edm-connector-protobuf",
    author="Thorkild Stray",
    author_email="thorkild.stray@cognite.com",
    install_requires=[
        "setuptools",
        "protobuf>=3.0.0,<4.0.0"
    ],
    python_requires=">=3.5",
    packages=find_namespace_packages(include=["cognite.*"]),
    package_data={'': ['edm_native_v1_pb2.pyi']},
)
