"""Dynamic configuration for setuptools."""
import os
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

with open(os.path.join('wait4localstack', 'VERSION')) as version_file:
    version = version_file.read().strip()

setuptools.setup(
    name='wait4localstack',
    version=version,
    author='League of Crafty Programmers Ltd.',
    author_email='info@locp.co.uk',
    description='Python utilities for ensuring that localstack has fully started.',
    entry_points={
        'console_scripts': ['wait4localstack=wait4localstack:main']
    },
    install_requires=['urllib3>=1.26.0'],
    keywords='localstack',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/locp/wait4localstack',
    package_data={
        '': ['VERSION']
    },
    project_urls={
        'Bug Tracker': 'https://github.com/locp/wait4localstack/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': '.'},
    packages=setuptools.find_packages(where='.'),
    python_requires='>=3.6')
