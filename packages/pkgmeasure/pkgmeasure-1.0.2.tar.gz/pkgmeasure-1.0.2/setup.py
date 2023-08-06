from setuptools import find_packages, setup

setup(
    # Needed to silence warnings
    name='pkgmeasure',
    url='https://github.com/jladan/package_demo',
    author='John Ladan',
    author_email='jladan@uwaterloo.ca',
    # Needed to actually package something
    packages=find_packages(where="pkgmeasure"),
    version='1.0.2',
    license='MIT',
    description='An example of a python package from pre-existing code',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.rst').read()
)
