from setuptools import find_packages, setup
from typing import List


HYPEN_E_DOT = "-e ."


def get_requirements(file_path: str) -> List[str]:
    """
    this function return the list of requirements
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements


setup(
    name="HACryptoAnalysis",
    version="0.0.2",
    author="Hector Gonzalez - Abdelaziz el Kadi",
    author_email="azizelkadi24@gmail.com",
    packages=find_packages(),
    description="A web app to analyse cryptocurrency prices and use technical indicators",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/azizelkadi/Proyecto-python",
    install_requirements=get_requirements("requirements.txt"),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts':[
            'HACryptoAnalysis=crypto_analysis.run:main'
        ]
    }
)