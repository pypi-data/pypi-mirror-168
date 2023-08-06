#!/usr/bin/env python3
# coding=utf-8

"""Python distribute file.

"""

from setuptools import setup, find_packages


def get_version_from_init_file():
    """parse version info from __init__.py file.

    Return the version string.

    """
    with open("redisexport/__init__.py", "r") as f:
        for line in f:
            if "__version__" in line:
                return line.split('"')[1]
    raise Exception("__version__ not found in redisexport/__init__.py")


def requirements_file_to_list(fn="requirements.txt"):
    """read a requirements file and create a list that can be used in setup.

    """
    with open(fn, 'r') as f:
        return [x.rstrip() for x in list(f) if x and not x.startswith('#')]


setup(
    name="redis-export",
    version=get_version_from_init_file(),
    packages=find_packages(exclude=("utils",)),
    install_requires=['redis'],
    entry_points={
        'console_scripts': [
            'redis-export = redisexport.main:redis_export',
            'redis-import = redisexport.main:redis_import',
        ]
    },
    package_data={
        # 'redisexport': ['logger.conf']
    },
    author="Yuanle Song",
    author_email="sylecn@gmail.com",
    maintainer="Yuanle Song",
    maintainer_email="sylecn@gmail.com",
    description="Export redis keys with a prefix or matching a pattern, import from exported file",
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    license="GPLv3+",
    url="https://pypi.org/project/redis-export/",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
