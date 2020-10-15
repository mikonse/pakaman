from setuptools import setup

VERSION = "0.1.0"
AUTHOR = "Michael Loipführer"


def readme():
    with open("README.md") as f:
        return f.read()


setup(name="pakaman",
      version=VERSION,
      description="Python package creation for all dem linuxes",
      long_description=readme(),
      url="http://github.com/mikonse/pakaman",
      classifiers=[
          "Development Status :: 5 - Production/Stable", "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3.7", "Operating System :: POSIX :: Linux"
      ],
      author=AUTHOR,
      author_email="ml@stusta.de",
      install_requires=["PyYAML", "schema", "Jinja2"],
      license="MIT",
      packages=["pakaman"],
      entry_points={"console_scripts": ["pakaman=pakaman.cli:cli"]},
      include_package_data=True,
      zip_safe=False)
