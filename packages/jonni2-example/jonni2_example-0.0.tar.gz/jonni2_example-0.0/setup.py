from setuptools import setup, find_packages

setup(
    name='jonni2_example',
    version='0.0',
    author='jonni2',
    packages=find_packages('src'),
    package_dir={'':'src'},
    install_requires=['pybind11',],
)
