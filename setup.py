import setuptools


install_requires = [
    "click",
    "confluent-kafka[avro]>=1.9,<2",
    "mmh3",
    "prometheus_client",
    "pydantic",
    "sqlitedict",
]

dev_requires = install_requires + [
    "pip-tools",
    "pytest",
    "pytest-cov",
    "time-machine",
    "twine",
    "sphinx",
    "sphinx-autodoc-typehints",
]

packages = setuptools.find_packages()

setuptools.setup(
    name="fluvii",
    version="0.2.15",
    description="A simple Kafka streams implementation in Python using confluent-kafka-python",
    packages=packages,
    install_requires=install_requires,
    dev_requires=dev_requires,
    include_package_data=True,
    extras_require={"dev": dev_requires},
    entry_points={'console_scripts': ['fluvii = fluvii.cli.__main__:fluvii_cli']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
