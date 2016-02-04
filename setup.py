import os
from setuptools import setup

def read_file(file_name):
    return open(os.path.join(os.path.dirname(__file__), 'docs', file_name)).read()

setup(
    name='transmission-manager',
    description='Dynamically managing activity of Transmission BT Client in response to user events.',
    long_description=(read_file('README.md')),
    url='https://github.com/C-Codes/transmission-manager',
    author='Christoph Russ',
    author_email='chruss@gmx.de',
    platforms=['any'],
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Topic :: Communications :: File Sharing',
        'Topic :: Communications',
        'Development Status :: 1 - Planning',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
)
