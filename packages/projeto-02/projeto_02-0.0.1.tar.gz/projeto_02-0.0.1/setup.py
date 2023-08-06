from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="projeto_02",
    version="0.0.1",
    author="Igor Mata",
    author_email="igor@mata.com.br",
    description="Projeto 2 DIO / Unimed",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/igorjvmata/Projeto_02"
)