import os

from setuptools import setup

ROOT = os.path.dirname(os.path.realpath(__file__))

setup(
    # Meta data
    name='nsfw',
    version='0.1.2',
    author='Muhammad Azhar',
    author_email='azhar@contentstudio.io',
    maintainer='Muhammad Azhar',
    maintainer_email='azhar@contentstudio.io',
    url='https://contentstudio.io',
    description='NSFW content analyzer',
    long_description=open(os.path.join(ROOT, 'README.md')).read(),
    license='MIT License',
    # Package files
    packages=[
        'nsfw',
    ],
    include_package_data=True,
    # Dependencies
    install_requires=[
        'requests',
        'lxml',
        'nltk',
        'pybloom_live',
    ],
    extras_require={
        'full': ['urllib3', 'certifi'],
    },
    test_suite='nose.collector',
    tests_require=['nose'],
)