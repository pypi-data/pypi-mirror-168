import setuptools
import time

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='lineage_keeper',  
     version='0.2',
     description="A lightweight lineage tool based on Spark and Delta Lake",
     url="https://github.com/otacilio-psf/lineage-keeper",
     author="Otacilio Filho",
     author_email="otaciliopedro@gmail.com",
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     packages=setuptools.find_packages(),
     install_requires=[
         'networkx>=2.6.3',
         'pyvis>=0.2.1'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
 )