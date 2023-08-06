import setuptools


def readme():
    with open('README.md') as f:
        return f.read()


setuptools.setup(
    name="treasurycurves",
    version="1.0.4",
    author="Danny Fryer",
    author_email="17fryerd@gmail.com",
    description=("query and analyze US Treasury yield data"),
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    py_modules=["treasury"],
    license="MIT",
    url="https://github.com/pepe454/treasury-curves",
    keywords="treasury",
    entry_points={
        "console_scripts": ["treasury=treasury:main"]
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Topic :: Office/Business :: Financial :: Investment",
        "Operating System :: Microsoft",
        "Natural Language :: English",
        "Development Status :: 4 - Beta",
        "License :: Freely Distributable",
        "Framework :: Pytest",
    ],
    install_requires=[
        "pandas",
        "requests",
        "matplotlib"
    ],
    project_urls={
        "Bug Tracker":"https://github.com/pepe454/treasury-curves/issues",
        "Documentation": "https://treasury-curves.readthedocs.io/en/latest/",
        "Source Code":"https://github.com/pepe454/treasury-curves",
    }
)
