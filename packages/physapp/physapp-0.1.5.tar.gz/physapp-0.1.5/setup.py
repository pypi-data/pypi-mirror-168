import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="physapp", # Replace with your own username
    version="0.1.5",
    author="David THERINCOURT",
    author_email="dtherincourt@gmail.com",
    description="Librairie Python pour la physique appliquée au lycée",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/david-therincourt/physapp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
