from setuptools import find_packages, setup

setup(
   name='yacloud',
   version='0.1.0',
   author='Dima Frolenko',
   author_email='orangefrol@gmail.com',
   packages=find_packages(),
#    entry_points = {
#         'console_scripts': ['nf=nf_lite.command_line:main'],
#    },
   license='LICENSE.txt',
   description='A micro package for working with yandex cloud services',
   long_description=open('README.txt').read(),
   install_requires=open('requirements.txt').readlines()
)