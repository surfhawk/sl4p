import platform
from setuptools import setup, find_packages
from os import path
import sys

# python2 setup.py bdist_wheel --plat-name=manylinux1_x86_64
# python3 setup.py bdist_wheel --plat-name=win_amd64
# python -m twine upload .\dist\sl4p-*.whl

readme_dir = path.dirname(__file__)
print("README doc's path : {}".format(path.join(readme_dir, "README.md")))

if sys.version_info[0] < 3:
    with open(path.join(readme_dir, "README.md")) as f:
        long_description = f.read()
else:
    with open(path.join(readme_dir, "README.md"), encoding='utf-8') as f:  # for python 3
        long_description = f.read()

requires = ['psutil', 'colorlog==6.7.0']
if 'windows' in platform.system().lower():
    requires.append('pywin32')
    requires.append('colorama')

setup(
    name='sl4p',
    version='1.4.3',
    description='Simple logger for python. Easy configuration and Multiprocess supported.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='surfhawk',
    author_email='surfhawk@naver.com',
    url='https://github.com/surfhawk/sl4p',
    python_requires='>=3.0',
    # py_modules=['sl4p'],
    packages=find_packages(exclude=['sl4p_examples']),
    include_package_data=True,
    package_data={
        'sl4p': ['*', 'mconfigs/*']
    },
    install_requires=requires,
    license='S-BSD',
    classifiers=[
        'Topic :: Utilities',
        'Topic :: System :: Logging',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.5'
    ],
)
