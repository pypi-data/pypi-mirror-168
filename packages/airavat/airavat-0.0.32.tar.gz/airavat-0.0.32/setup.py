import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="airavat",
    version="0.0.32",
    author="Saumitra Rawat",
    author_email="saumitra.rawat@gmail.com",
    description="Audit Utilities for Azure Data Factory- To find the common engineering hacks and reduce manual "
                "interventions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Saumitra24/airavat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
