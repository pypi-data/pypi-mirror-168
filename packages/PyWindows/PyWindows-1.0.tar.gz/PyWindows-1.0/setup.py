from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PyWindows",
    version="1.0",
    description="Windows for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src", "lib": "src/PyWindows/lib"},
    include_package_data=True,
    packages=find_packages(where="src"),
    author="Phoneguytech",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)