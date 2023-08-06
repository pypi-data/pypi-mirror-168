import sys

from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.read()
requirements = requirements.splitlines()

with open('README.md') as f:
    readme = f.read()
readme = "\n".join(readme.split('\n')[2:])

packages = find_packages()

with open('deqart/version.py') as f:
    Version = f.read()

Version = Version.rstrip()
Version = Version[15:-1]

setup(
    name='deqart',
    version=Version,
    description='Python SDK to Deqart platform',
    license='Apache',
    author='BlueQubit',
    author_email='hovnatan@bluequbit.io',
    url='https://github.com/BlueQubitDev/deqart-python-sdk',
    long_description=readme,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    setup_requires=['wheel'],
    packages=find_packages(exclude=('tests', )),
    entry_points={
        'console_scripts': ['deqart = deqart.__main__:main']
    },
    python_requires='>=3.6'
)
