"""
Type this in terminal to upgrade the package.
>> python setup.py sdist bdist_wheel
>> twine upload dist/*
"""
from setuptools import find_packages, setup

setup(name="handyplot",
      version="0.3.2",
      description="Add line scatter and color lib.",
      author="Hong Peng",
      python_requires=">=3.8.0",
      url="https://github.com/minho-hong/handyplot.git",
      package_data={},
      packages=find_packages(),
      install_requires=["matplotlib", "numpy", "vtk"],
      license="GPL")