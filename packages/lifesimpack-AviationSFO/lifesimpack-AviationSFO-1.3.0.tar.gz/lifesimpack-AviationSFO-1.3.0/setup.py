import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lifesimpack-AviationSFO",
    version="1.3.0",
    author="Steven Weinstein",
    author_email="srw08sf@gmail.com",
    description="A life \'simulation\' package created as a joke.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AviationSFO/lifesimpack",
    project_urls={
        "Bug Tracker": "https://github.com/AviationSFO/lifesimpack/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)