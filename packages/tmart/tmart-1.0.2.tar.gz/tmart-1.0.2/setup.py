import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tmart",                     # This is the name of the package
    version="1.0.2",                        # The initial release version
    author="Yulun Wu",                     # Full name of the author
    description="Radiative transfer modelling of the adjacency effect in aquatic remote sensing",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    # packages=setuptools.find_packages(),    # List of all python modules to be installed
    packages = ['tmart','tmart.ancillary','tmart.ancillary.aerosolSPF'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    # py_modules=["tmart"],             # Name of the python package
    # package_dir={'':'tmart/'},     # Directory of the source code of the package
    license_files=('license'),
    install_requires=['Py6S','numpy','pandas','scipy','pathos','matplotlib']  # Install other dependencies if any
)