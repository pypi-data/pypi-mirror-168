from setuptools import setup
from setuptools import find_packages

README = ''.join([line for line in open("README.md").readlines()])
setup(
    name="swt-nlp",
    version="0.0.23",
    author="@muuusiiik",
    author_email="muuusiiikd@gmail.com",
    description="simple nlp pipeline",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    python_requires=">=3.7",
    license="Apache Software License 2.0",
     classifiers=[
         "License :: OSI Approved :: Apache Software License",
         "Programming Language :: Python :: 3",
         "Programming Language :: Python :: 3.7",
     ],
     #packages=["muuusiiik"],
     packages=find_packages("."),

     # DEAL WITH DATA
     #package_data={"vocab": ["vocab/*"]}
     #include_package_data=True,

     # DEPENDENCIES PACKAGES
     install_requires=[
         "muuusiiik",
         "pandas",
         "marisa-trie",
         "pythainlp",
         "scikit-learn",
         ],
 )

