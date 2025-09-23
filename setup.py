from setuptools import find_packages, setup
from typing import List

hyphen_e = '-e .'

def get_requirements(file_path: str) -> List[str]:
    # this function will return list of requirements
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [require.replace('\n', '') for require in requirements]

        if hyphen_e in requirements:
            requirements.remove(hyphen_e)

    return requirements


setup(
    name='mlproject',
    version='0.0.1',
    author='pk-790324',
    author_email='pappuyadav98199@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
