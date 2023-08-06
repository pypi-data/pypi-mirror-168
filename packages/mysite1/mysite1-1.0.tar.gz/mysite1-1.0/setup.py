# # setup.py
# from setuptools import setup
# setup(name='mysite1',
# version='0.1',
# description='this is a tet lib',
# url='#',
# author='auth',
# author_email='author@email.com',
# license='MIT',
# packages=['mysite1'],
# zip_safe=False)

from distutils.core import  setup
packages = ['mysite1']# 唯一的包名，自己取名
setup(name='mysite1',
	version='1.0',
	author='wjl',
    packages=packages,
    package_dir={'requests': 'requests'},)
