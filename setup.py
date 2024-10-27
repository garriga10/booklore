from setuptools import find_packages, setup

# We first select all the packages of the requirements.txt file and we
# put them in the format of a list inside requirements

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

# We define a tuple object called setup that puts together the name, version,
# packages requirements and passes a find_packages function in the packages
# variable.

setup(
    name='package_folder',
    version="0.0.1",
    install_requires=requirements,
    packages=find_packages()
)
