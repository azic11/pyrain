from setuptools import setup

setup(
    name='pyraincloud',
    version='0.0.1',
    description='A python module to draw raincloud plots',
    author='Anton Zickler',
    author_email='anton.zickler@gmail.com',
    pymodules=['pyraincloud'],
    install_requires=[
        'numpy',
        'matplotlib',
    ],
)

