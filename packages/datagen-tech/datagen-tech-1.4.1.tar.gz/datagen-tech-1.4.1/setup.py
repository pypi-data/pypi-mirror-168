from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="datagen-tech",
    version="1.4.1",
    description="Datagen SDK",
    long_description_content_type="text/markdown",
    long_description=long_description,
    license="Apache License 2.0",
    author="Datagen Technologies Ltd.",
    url="https://datagen.tech/",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "dependency-injector>=4.6",
        "marshmallow-dataclass>=6,!=8.5.4,!=8.5.5,!=8.5.6,!=8.5.7,!=8.5.8",
        "marshmallow-enum>=1.5",
        "matplotlib>=3",
        "numpy>=1",
        "scipy>=1.4",
        "pillow>=7.0",
        "tqdm>=4.6",
        "opencv-python>=4.4",
        "jupyter>=1.0",
        "Deprecated>=1.2",
        "pydantic>=1.9",
        "rich>=12.5",
        "beautifulsoup4",
        "dynaconf>=3.0"
    ],
    include_package_data=True,
    python_requires=">=3.6",
)
