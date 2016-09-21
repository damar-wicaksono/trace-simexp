from setuptools import setup


setup(name="trace-simexp",
      version="0.3.0",
      description="Script utility to assist simulation experiment with TRACE",
      url="https://bitbucket.org/lrs-uq/trace-simexp",
      author="Damar Wicaksono",
      author_email="damar.wicaksono@gmail.com",
      license="MIT",
      packages=["trace_simexp"],
      scripts=["bin/trace_simexp_create_h5"],
      entry_points={
        "console_scripts": [
              "trace_simexp_prepro=trace_simexp.command_line:prepro",
              "trace_simexp_execute=trace_simexp.command_line:execute",
              "trace_simexp_postpro=trace_simexp.command_line:postpro"
        ]
      },
      zip_safe=False)
