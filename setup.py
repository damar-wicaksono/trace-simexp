from setuptools import setup


setup(name="trace-simexp",
      version="0.3.1",
      description="Script utility to assist simulation experiment with TRACE",
      url="https://bitbucket.org/lrs-uq/trace-simexp",
      author="Damar Wicaksono",
      author_email="damar.wicaksono@gmail.com",
      license="MIT",
      packages=["trace_simexp"],
      scripts=["bin/trace_simexp_prepro", "bin/trace_simexp_execute",
               "bin/trace_simexp_postpro", "bin/trace_simexp_create_h5"],
      zip_safe=False)
