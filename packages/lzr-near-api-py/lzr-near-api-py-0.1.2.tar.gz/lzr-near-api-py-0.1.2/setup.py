from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

META_DATA = dict(
    name="lzr-near-api-py",
    version="0.1.2",
    license="MIT",

    author="NEAR Inc",

    url="https://github.com/near/near-api-py",

    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),

    install_requires=["requests", "urllib3", "base58", "ed25519"]
)

if __name__ == "__main__":
    setup(**META_DATA)
