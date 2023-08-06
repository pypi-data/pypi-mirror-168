import setuptools

with open("README.md", "r") as file_obj:
    long_description = file_obj.read()

install_requires = [
    "confluent-kafka[avro]==1.8.2",
    "dictdiffer",
    "mmh3",
    "prometheus_client",
    "psutil",
    "python-box",
    "python-dateutil",
    "python-dotenv",
    "python_eloqua_wrapper",
    "pytz",
    "pyyaml",
    "requests",
    "simple_salesforce",
    "virtualenv",
    "virtualenv-api",
    "wrapt-timeout-decorator",
    "sqlitedict",
]

dev_requires = install_requires + [
    "pip-tools",
    "pytest",
    "pytest-cov",
    "time-machine",
    "twine",
]

packages = setuptools.find_packages()

setuptools.setup(
    name="nubium-utils",
    author="Edward Brennan",
    author_email="ebrennan@redhat.com",
    description="Some Kafka utility functions and patterns for the nubium project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.corp.redhat.com/mkt-ops-de/nubium-utils.git",
    packages=packages,
    install_requires=install_requires,
    include_package_data=True,
    extras_require={"dev": dev_requires},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
