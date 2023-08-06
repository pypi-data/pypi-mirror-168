from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="processamento_de_imagem2",
    version="0.0.5",
    author="Leonardo Henrique Martins",
    author_email="leo.he.martins@gmail.com",
    description="Projeto DIO",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LeonardoHMartins/image_processing-test",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
