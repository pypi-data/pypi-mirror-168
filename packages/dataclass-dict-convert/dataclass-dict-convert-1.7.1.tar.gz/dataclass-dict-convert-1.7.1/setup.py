from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dataclass-dict-convert",
    version="1.7.1",

    description="Convert between Dataclasses and dict/json",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://gitlab.ilabt.imec.be/wvdemeer/dataclass-dict-convert",

    author="Wim Van de Meerssche",
    author_email="wim.vandemeerssche@ugent.be",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],

    packages=["dataclass_dict_convert"],
    include_package_data=True,

    install_requires=[
        "python-dateutil",
        "stringcase",  # used in tests, AND typically by users of the lib. But not by the lib itself.
    ],
    python_requires='>=3.7',   # python >= 3.7 because python dataclasses are required

    # Tests with py.test:  run with: python setup.py pytest
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    zip_safe=False,
)
