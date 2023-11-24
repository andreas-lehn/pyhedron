from setuptools import setup

setup(
    name='pyhedron',
    version='0.1.0',    
    description='A Polyhedron implemented in Python',
    url='https://github.com/andreas-lehn/pyhedron',
    author='Andreas Lehn',
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
