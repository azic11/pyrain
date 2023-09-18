from setuptools import setup

setup(
    name='pyrain',
    version='0.0.1',
    description='A python module to draw raincloud plots',
    author='Anton Zickler',
    author_email='anton.zickler@gmail.com',
    py_modules=['pyrain'],
    install_requires=[
        'numpy',
        'matplotlib',
    ],
)

