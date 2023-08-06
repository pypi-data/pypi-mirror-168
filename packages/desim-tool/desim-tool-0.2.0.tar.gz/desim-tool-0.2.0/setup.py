import setuptools

setuptools.setup(
name='desim-tool',
version='0.2.0',
license='MIT',
description='A discrete event simulator',
url='https://github.com/sed-group/desim',
author='Erik',
install_requires=['simpy', 'numpy'],
author_email='eber@chalmers.se',
packages=setuptools.find_packages())