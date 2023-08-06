version = "0.1.1"
install_requires = [
]

from setuptools import setup, find_packages

setup(
    name = "benimang",
    version = version,
    keywords="beni",
    description = "utils library for Beni",
    license = "MIT License",
    url = "https://pytask.com",
    author = "Beni",
    author_email = "benimang@126.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = install_requires,
    entry_points={
        "console_scripts": ["beni=beni.bcmd:main"],
    },
)