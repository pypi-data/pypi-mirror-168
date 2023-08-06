from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'safe_ase'
LONG_DESCRIPTION = 'helper functions wrapping ase fucntions that dont overwrite original structure'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="safe_ase", 
        version=VERSION,
        author="Roberto Rousse",
        author_email="<roberto.rousse@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'ase',
        ],
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
        ]
)