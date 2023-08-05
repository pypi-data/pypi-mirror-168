from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

META_DATA = dict(
    name="loozr-near-sdk",
    version="0.0.3",
    license="MIT",

    author="Loozr Inc",

    url="https://github.com/Loozr-Protocol/loozr-near-py",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["lzr-near-api-py"]
)

if __name__ == "__main__":
    setup(**META_DATA)
