from setuptools import find_packages, setup


setup(
    name="parrotschemas",
    description="Protobuf schemas for Parrot.",
    url="https://github.com/parrot-com/schemas",
    project_urls={"Source Code": "https://github.com/parrot-com/schemas"},
    author="Parrot",
    maintainer="Parrot",
    keywords=["protobuf", "schemas"],
    version="0.1.5",
    long_description="Protobuf schemas for Parrot.",
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=["protobuf>=3.17.3"],
    include_package_data=True,
)
