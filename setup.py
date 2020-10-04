# -*- coding: utf-8 -*-
"""
Setup install script for volmdlr

"""

from setuptools import setup
# from distutils.core import setup

from os.path import dirname, isdir, join
import re
from subprocess import CalledProcessError, check_output

tag_re = re.compile(r'\btag: %s([0-9][^,]*)\b')
version_re = re.compile('^Version: (.+)$', re.M)


def readme():
    with open('README.md') as f:
        return f.read()


def get_version():
    # Return the version if it has been injected into the file by git-archive
    version = tag_re.search('$Format:%D$')
    if version:
        return version.group(1)

    d = dirname(__file__)

    if isdir(join(d, '.git')):
        cmd = 'git describe --tags'
        try:
            version = check_output(cmd.split()).decode().strip()[:]
        except CalledProcessError:
            raise RuntimeError('Unable to get version number from git tags')
        if version[0] == 'v':
            version = version[1:]
        # PEP 440 compatibility
        if '-' in version:
            future_version = version.split('-')[0].split('.')
            if 'post' in future_version[-1]:
                future_version = future_version[:-1]
            future_version[-1] = str(int(future_version[-1]) + 1)
            future_version = '.'.join(future_version)
            number_commits = version.split('-')[1]
            version = '{}.dev{}'.format(future_version, number_commits)
            return version

    # else:
    #     # Extract the version from the PKG-INFO file.
    #     with open(join(d, 'PKG-INFO')) as f:
    #         version = version_re.search(f.read()).group(1)

    #    # Writing to file
    #    with open('powertransmission/version.py', 'w+') as vf:
    #        vf.write("# -*- coding: utf-8 -*-\nversion = '{}'".format(version))

    return version


setup(name='business_plan',
      version=get_version(),
      #      setup_requires=['setuptools_scm'],
      description=' A library for the business plan definition ',
      #long_description=readme(),
      keywords='business, plan',
      url='https://documentation.dessia.tech/BusinessPlan',
      author='Pierre-Emmanuel Dumouchel',
      author_email='dumouchel@dessia.tech',
      packages=['business_plan'],
      package_dir={},
      include_package_data=True,
      install_requires=['numpy', 'matplotlib', 'scipy'],
      classifiers=['Topic :: Scientific/Engineering', 'Development Status :: 3 - Alpha'])
