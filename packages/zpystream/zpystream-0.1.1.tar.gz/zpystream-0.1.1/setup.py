from setuptools import (
    find_packages,
    setup,
)

setup(
    name='zpystream',
    version='0.1.1',
    description='zpystream',
    classifiers=[],
    keywords='zpystream',
    author='zgl',
    author_email='',
    url='',
    license='MIT',
    packages=find_packages(exclude=[]),
    package_data={'': ['*.*']},
    include_package_data=True,
    install_requires=[],
    long_description='python stream'
)
