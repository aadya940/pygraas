from setuptools import setup, find_packages

setup(
    name="pygraas",
    version="0.1.0",
    author="Aadya Chinubhai, Amit Nanavati",
    author_email="aadyachinubhai@gmail.com",
    description="A Python Library for Graph Analytics for Security in Python Packages",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aadya940/pygraas",
    packages=find_packages(),
    install_requires=[
        "pydot",
        "matplotlib",
        "pydeps",
        "networkx",
        "networkx-gdf",
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
