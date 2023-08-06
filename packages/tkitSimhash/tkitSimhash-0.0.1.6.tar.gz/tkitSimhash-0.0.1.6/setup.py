from setuptools import setup
import os
from os import path as os_path
this_directory = os_path.abspath(os_path.dirname(__file__))
# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description
long_description=read_file("README.md")
setup(
    name='tkitSimhash',
    version='0.0.1.6',
    packages=['tkitSimhash'],
    url='https://terrychanorg.jetbrains.space/p/tkittools/repositories/tkitRemoveDuplicates/files/master/README.md',
    license='',
    author='Terry Chan',
    author_email='napoler2008@gmail.com',
    description= long_description[:256],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'jieba>=0.42.1',
        'simhash==2.1.2',
        'nltk>=3.6',
        'pytest==7.1.3'
        ]


)
