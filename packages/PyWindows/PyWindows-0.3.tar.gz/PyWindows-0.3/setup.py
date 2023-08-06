from setuptools import setup, find_packages

setup(
    name="PyWindows",
    version=0.3,
    description="Windows for Python",
    long_description="AAA",
        package_dir={"": "src"},
    packages=find_packages(where="src"),
    author="Phoneguytech"
)