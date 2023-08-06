import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eazysdk",
    version="1.3.0",
    author="Eazy Collect",
    author_email="help@eazycollect.co.uk",
    description="A Python SDK client to interact with Eazy Customer Manager 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EazyCollectServices/EazyCollectSDK-Python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)