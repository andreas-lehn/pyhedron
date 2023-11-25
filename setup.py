from setuptools import setup
from pathlib import Path
import gitversion

NAME = 'pyhedron'
AUTHOR = 'Andreas Lehn'
VERSION = gitversion.get()
README = 'readme.rst'

gitversion.create_version_file(NAME, VERSION)

readme_file = Path(__file__).parent / "readme.rst"

setup(
    name='pyhedron',
    version=VERSION,    
    description='A Polyhedron implemented in Python',
    long_description=readme_file.read_text(),
    long_description_content_type='text/x-rst',
    url='https://github.com/andreas-lehn/pyhedron',
    author="Andreas Lehn",
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
