from setuptools import find_packages, setup

with open("README.md", "r") as f:
  long_description = f.read()

setup(
  name = 'pyslvSudoku',
  packages = find_packages(),
  include_package_data=True,
  version = '0.1',
  license='MIT',
  description = 'Simple package fro solving a sudoku',
  author = 'Subhradipta Paul',
  author_email = 'paulsubhradipta@gmail.com',
  keywords = ['sudoku'],
  long_description=long_description,
  long_description_content_type="text/markdown",
  classifiers=[
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
