import re

from setuptools import find_packages, setup

with open("src/parrottools/__version__.py", encoding="utf8") as f:
    data = f.read()
    version = re.search(r'__version__ = "(.*?)"', data).group(1)  # type: ignore
    title = re.search(r'__title__ = "(.*?)"', data).group(1)  # type: ignore

install_requires = []
with open("requirements.txt") as f:
    for line in f.read().splitlines():
        if line.startswith("#") or line.strip() == "":
            continue
        else:
            install_requires.append(line)

setup(
    name=title,
    description="Collection of common utilities.",
    url="https://github.com/parrot-com/parrottools",
    project_urls={"Source Code": "https://github.com/parrot-com/parrottools"},
    author="Parrot",
    maintainer="Parrot",
    keywords=["observability", "logging"],
    version=version,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=install_requires,
    extras_require={
        "tests": ["pytest>=6.2.1", "freezegun==1.1.0"],
        "dev": ["pytest>=6.2.1", "pre-commit>=2.9.3"],
    },
    include_package_data=True,
)
