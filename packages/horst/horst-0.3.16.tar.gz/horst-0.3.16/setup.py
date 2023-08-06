import setuptools
"""
    usage to build pypi package
    
    create distribution
    $ python setup.py sdist

    build wheel
    $ python setup.py bdist_wheel
"""
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name='horst',  
    version='0.3.16',
    author="Frank T. Maas",
    author_email="frank.maas@funkemedien.de",
    description="Do not repeat yourself in SQL scripts by listing the same fields again and again.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/FMG_ULM/horst",
    packages=["horst",],
    entry_points = {
        "console_scripts": ['aogl = aogl.aogl:main']
    },
    install_requires=[
        "sly"
        ,
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)