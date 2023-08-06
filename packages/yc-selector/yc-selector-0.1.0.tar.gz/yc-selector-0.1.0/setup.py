from setuptools import find_packages, setup

setup(
   name='yc-selector',
   version='0.1.0',
   author='Dima Frolenko',
   author_email='orangefrol@gmail.com',
   packages=find_packages(),
#    entry_points = {
#         'console_scripts': ['nf=nf_lite.command_line:main'],
#    },
   license='LICENSE.txt',
   description='Yandex Cloud module for routing cloud functions',
   long_description=open('README.txt').read(),
   install_requires=open('requirements.txt').readlines()
)