from os.path import abspath, dirname, join

from setuptools import find_packages, setup

PWD = dirname(abspath(__file__))
f = open(join(PWD, "README.MD"))
README = f.read()

setup(
    name="flatten_nosql",
    version="2.2",
    author="Masum Billal",
    author_email="billalmasum93@gmail.com",
    url="https://github.com/proafxin/nosql-to-sql",
    description="This module converts NoSQL data to plain SQL data.",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=[
        "flattener",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["pandas"],
    license="MIT",
    # entry_points={
    #     'console_scripts': [
    #         'flattennosql=flattener.flatten',
    #     ],
    # },
)
