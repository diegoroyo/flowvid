import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flowvid",
    version="0.4.0",
    author="Diego Royo",
    author_email="740388@unizar.es",
    description="Optical Flow video tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diegoroyo/flowvid",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)