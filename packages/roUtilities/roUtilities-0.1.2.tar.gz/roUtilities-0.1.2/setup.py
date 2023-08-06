from setuptools import setup, find_packages


setup(
    name='roUtilities',
    version='0.1.2',
    description='Adds an utilities, that rorosin needs in his projects.',
    license="MIT",
    author="rorosin",
    long_description=open('README.md').read(),
    url='https://github.com/Anton-Rosin-Dev/roUtilities/',
    install_requires=["colorama>=0.4.5"],
    packages=find_packages(exclude=['tests']),
)