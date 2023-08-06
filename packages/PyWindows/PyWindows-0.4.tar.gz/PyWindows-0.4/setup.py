from setuptools import setup, find_packages

setup(
    name="PyWindows",
    version=0.4,
    description="Windows for Python",
    long_description="long_description",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    author="Phoneguytech"
)