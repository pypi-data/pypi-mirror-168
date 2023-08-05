from setuptools import find_packages, setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zqmtool",
    version="0.0.52",
    author="qiming_zou",
    author_email="zqm1028@gmail.com",
    description="qiming zou's toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages('src'),
    python_requires=">=3.6",
)
