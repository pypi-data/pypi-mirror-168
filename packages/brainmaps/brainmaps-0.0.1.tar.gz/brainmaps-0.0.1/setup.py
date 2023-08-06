from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="brainmaps",
    version="0.0.1",
    author="Alex Harston",
    author_email="alex@harston.io",
    description="A command-line client to the BrainMaps platform.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexharston/brainmaps-cli",
    license="MIT",
    python_requires='>=3',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='brainmaps, brainmaps-api, atlas, anatomy',
    packages=find_packages(),
    install_requires=['argparse',],
)
