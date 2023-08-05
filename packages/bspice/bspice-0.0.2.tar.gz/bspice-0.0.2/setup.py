import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bspice",
    version="0.0.2",
    author="Behrouz Safari",
    author_email="behrouz.safari@gmail.com",
    description="Working with SPICE kernels",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/behrouzz/bspice",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["bspice"],
    include_package_data=True,
    install_requires=["numpy", "requests", "spiceypy"],
    python_requires='>=3.6',
)
