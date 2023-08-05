from setuptools import setup, find_packages


setup(
    name='roUtilities',
    version='0.1',
    description='Adds an utilities, that rorosin needs in his projects.',
    license="MIT",
    author="rorosin",
    long_description=open('README.md').read(),
    url='https://github.com/Anton-Rosin-Dev/roUtilities/',
    install_requires=[],
    packages=find_packages(exclude=['tests']),
)