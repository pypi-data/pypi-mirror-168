from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="imecilabt-utils",
    version="1.6.0",

    description="A collection of functions useful in various projects iLab.t projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://gitlab.ilabt.imec.be/ilabt/imecilabt-py-utils",

    author="Wim Van de Meerssche",
    author_email="wim.vandemeerssche@ugent.be",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],

    packages=["imecilabt_utils"],
    include_package_data=True,

    install_requires=[],
    python_requires='>=3.5',

    # Tests with py.test:  run with: python setup.py pytest
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    zip_safe=False,
)
