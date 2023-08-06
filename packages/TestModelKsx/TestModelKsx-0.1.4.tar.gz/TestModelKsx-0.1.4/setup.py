from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as f:
  long_description = f.read()

setup(name='TestModelKsx',  # 包名
      version='0.1.4',  # 版本号
      description='A small example package',
      long_description=long_description,
      author='ksx',
      author_email='ksx@shu.edu.cn',
      install_requires=['tensorflow'],
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
