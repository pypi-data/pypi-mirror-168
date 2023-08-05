from pathlib import Path
from setuptools import find_packages, setup
dependencies = [ ]
# read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='uniocsone',
    packages=find_packages(),
    version='0.0.5',
    description='Uni to OCSone',
    author='OCS',
    author_email='ztmaung@ocsmandalay.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    project_urls={
        "Bug Tracker": "https://github.com/",
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=dependencies,
)