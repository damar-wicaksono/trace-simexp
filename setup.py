"""A setuptools based setup module for trace-simexp

"""
from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

exec(open('trace_simexp/_version.py').read())
setup(
      name="trace-simexp",

      # Versions comply with semantic versioning, see
      # http://semver.org/
      version=__version__,

      description="Script utility to assist simulation experiment with TRACE",
      long_description=long_description,

      # The project's main homepage
      url="https://bitbucket.org/lrs-uq/trace-simexp",

      # Author details
      author="Damar Wicaksono",
      author_email="damar.wicaksono@gmail.com",

      license="MIT",

      # Classifiers
      classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developer",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.5"
      ],

      # Manually entered package name
      packages=["trace_simexp"],

      # Provide the following executable scripts
      entry_points={
        "console_scripts": [
              "trace_simexp_prepro=trace_simexp.command_line:prepro",
              "trace_simexp_execute=trace_simexp.command_line:execute",
              "trace_simexp_postpro=trace_simexp.command_line:postpro"
        ]
      },

      zip_safe=False
)
