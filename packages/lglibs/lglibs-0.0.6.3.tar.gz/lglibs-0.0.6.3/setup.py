import setuptools


version = "0.0.6.3"

setuptools.setup(
    name="lglibs",  # This is the name of the package
    version=version,  # The initial release version
    author="Gao ZhenZhe",  # Full name of the author
    description="",
    author_email="2983536011@qq.com",
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["lglibs"],  # List of all python modules to be installed
    install_requires=[],
    python_requires='>=3.7',  # Minimum version requirement of the package
    zip_safe=False
)
