import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='yachtcharter',
      version='1.0.2',
      long_description=README,
      long_description_content_type="text/markdown",
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Information Analysis',
      ],
      keywords='data-visualization data data-visualisation data analysis',
      url='https://github.com/guardian/yacht-charter-python-library',
      author='Nick Evershed',
      author_email='nick.evershed@theguardian.com',
      license='MIT',
      packages=['yachtcharter'],
      install_requires=['boto3','simplejson'],
      zip_safe=False)