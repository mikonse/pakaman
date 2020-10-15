from setuptools import setup

VERSION = '1.0.0'
AUTHOR = 'Some Author'


def readme():
    with open("README.md") as f:
        return f.read()


setup(name='test_pkg',
      version=VERSION,
      description='small dummy test package',
      long_description=readme(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.8',
          'Operating System :: POSIX :: Linux'
      ],
      url="https://github.com/someuser/somepackage",
      author=AUTHOR,
      author_email='some-email@something.com',
      install_requires=[],
      license='MIT',
      packages=['src'],
      entry_points={'console_scripts': ['test_pkg=src.cli:cli']},
      include_package_data=True,
      zip_safe=False)
