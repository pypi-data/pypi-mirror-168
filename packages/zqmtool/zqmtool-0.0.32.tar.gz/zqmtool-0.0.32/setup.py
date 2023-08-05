import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="zqmtool",
    version="0.0.32",
    author="qiming_zou",
    author_email="zqm1028@gmail.com",
    description="qiming zou's toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url=" ,
    # project_urls=\{\},
    package_dir={"": "src_armed/"},
    packages=setuptools.find_packages(where="src_armed/"),
    python_requires=">=3.6",
)
