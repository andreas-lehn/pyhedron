from setuptools import setup
from pyhedron import __version__, __author__

setup(
    name='pyhedron',
    version=__version__,    
    description='A Polyhedron implemented in Python',
    url='https://github.com/andreas-lehn/pyhedron',
    author=__author__,
    author_email='andreas.lehn@icloud.com',
    license='MIT',
    packages=['pyhedron'],
    install_requires=[ 'numpy' ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',
    ],
)
