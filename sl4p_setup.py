from setuptools import setup, find_packages
from os import path
import sys

# python2 setup.py bdist_wheel
# python3 setup.py bdist_wheel

readme_dir = path.dirname(__file__)
print("README doc's path : {}".format(path.join(readme_dir, "README.md")))

if sys.version_info[0] < 3:
    with open(path.join(readme_dir, "README.md")) as f:
        long_description = f.read()
else:
    with open(path.join(readme_dir, "README.md"), encoding='utf-8') as f:  # for python 3
        long_description = f.read()


setup(
    name='sl4p',
    version='1.2.0',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Surfhawk',
    author_email='surfhawk@naver.com',
    url='https://github.com/TODO', #TODO
    python_requires='>=3.0',
    #py_modules=['sl4p'],
    packages=find_packages(exclude=['sl4p_examples']),
    include_package_data=True,
    package_data={
        'sl4p': ['*', 'mconfigs/*']
    },
    install_requires=[
    ],
    license='S-BSD',
    classifiers=[
        'Topic :: Utilities',
        'Topic :: System :: Logging',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.5'
    ]
)