import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="locksey",
    version="0.1.0",
    author="RainingComputers",
    author_email="vishnu.vish.shankar@gmail.com",
    description="Personal CLI utility tool to easily encrypt and decrypt files in a directory.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RainingComputers/locksey",
    packages=setuptools.find_packages(exclude=["docs", "tests"]),
    python_requires=">=3.8",
    install_requires=["cryptography"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
    keywords="locksey",
)
