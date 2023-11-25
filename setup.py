from setuptools import setup
from pathlib import Path
import gitversion

PACKAGE = 'pyhedron'
VERSION = gitversion.get()
gitversion.create_version_file(PACKAGE, VERSION)

setup(
    name=PACKAGE,
    version=VERSION,    
    description='A Polyhedron implemented in Python',
    long_description=(Path(__file__).parent / "readme.rst").read_text(),
    long_description_content_type='text/x-rst',
    url='https://github.com/andreas-lehn/pyhedron',
    author="Andreas Lehn",
    author_email='andreas.lehn@icloud.com',
    license='MIT',
    packages=[PACKAGE],
    install_requires=[ 'numpy' ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',
    ],
)
