# Copyright 2018 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from setuptools import setup, find_packages


setup(
  name='ctypes_test',
  version='0.0.1',
  packages=find_packages(),
  data_files=[('', ['libasdf-cpp_ctypes-with-extra-compiler-flags.so'])],
)
