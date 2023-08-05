import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cleverminer",
    version="1.0.2",
    author="(C) Copyright 2020 - 2022 Little Big Company, s.r.o.",
    author_email="code@cleverminer.org",
    description="Beyond apriori. Cleverminer is implementation of GUHA procedures that generalises apriori and association rules in many ways. Trully explainable knowledge mining.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://cleverminer.org",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
	"License :: Free for non-commercial use",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)