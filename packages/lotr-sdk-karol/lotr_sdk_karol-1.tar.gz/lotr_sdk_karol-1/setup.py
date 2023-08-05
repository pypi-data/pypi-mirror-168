from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read

setup(
    name='lotr_sdk_karol',
    version='1',
    description ='Lord of the rings SDK',
    py_modules=["lotr_sdk"],
    package_dir={'src':'./src'},

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires = [
        "certifi==2022.9.14",
        "charset-normalizer==2.1.1",
        "idna==3.4",
        "urllib3==1.26.12",
    ],
    author="Karol Djanashvili"
)