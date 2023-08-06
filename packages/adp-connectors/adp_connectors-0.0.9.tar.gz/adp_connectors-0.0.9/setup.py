from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="adp_connectors",
    version="0.0.9",
    description="connection clients for storage and database",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Hongfei Tian",
    author_email="hongfei.tian@ibm.com",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],

    keywords="connector, storage, database",
    packages=find_packages(),
    python_requires=">=3.8, <4",

    install_requires=[
        "pandas",
        "boto3",
        "boxsdk[jwt]",
        "psycopg2;platform_system=='Windows'",
        "psycopg2-binary;platform_system!='Windows'"
    ]
)
