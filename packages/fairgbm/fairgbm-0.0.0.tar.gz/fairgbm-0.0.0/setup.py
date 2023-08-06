from pathlib import Path
from setuptools import setup, find_packages


ROOT_PATH = Path(__file__).parent
README_PATH = ROOT_PATH / 'README.md'

setup(name='fairgbm',
      version='0.0.0',
      description='FairGBM Python Package',
      long_description_content_type="text/markdown",
      long_description=README_PATH.read_text(),
      install_requires=[
          'wheel',
      ],
      maintainer='Feedzai',
      zip_safe=False,
      packages=find_packages(),
      include_package_data=True,
      license='The Apache License 2.0 (Feedzai)',
      url='https://github.com/feedzai/fairgbm',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: MacOS',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX',
                   'Operating System :: Unix',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   'Topic :: Scientific/Engineering :: Artificial Intelligence'])
