from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mylingowell/__init__.py
from mylingowell import __version__ as version

setup(
	name="mylingowell",
	version=version,
	description="mylingowell",
	author="rakesh",
	author_email="rakesh@example.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
