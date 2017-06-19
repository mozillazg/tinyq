# -*- coding: utf-8 -*-
import sys
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()


def long_description():
    with open('README.rst', encoding='utf8') as f:
        return f.read()


requirements = [
    'redis',
]

setup(
    name='tinyq',
    version='0.3.0',
    description='A tiny job queue framework.',
    long_description=long_description(),
    url='https://github.com/mozillazg/tinyq',
    author='mozillazg',
    author_email='mozillazg101@gmail.com',
    license='MIT',
    package_data={'': ['LICENSE']},
    packages=['tinyq'],
    package_dir={'tinyq': 'tinyq'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'tinyq = tinyq.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    keywords='queue, 队列',
)
