from setuptools import setup
from setuptools import find_packages

version = "0.2"
requires = ["ordereddict", "jinja2", "configobj", "zope.component"]
long_description = open("README", "r").read() + "\n\n" \
                + open("CHANGES", "r").read()

setup(name="statics",
      version=version,
      description="Static site generator.",
      long_description=long_description,
      keywords="web publisher staticsite",
      author="Andrey Popp",
      author_email="8mayday@gmail.com",
      license="MIT",
      packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
      include_package_data=True,
      zip_safe=True,
      install_requires=requires,
      test_suite="statics.tests",
      entry_points={"console_scripts": "statics-init=statics.cli:statics_init"},
      )
