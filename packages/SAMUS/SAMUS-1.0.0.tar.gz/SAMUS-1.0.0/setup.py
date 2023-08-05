from setuptools import setup
import os

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return(file.read())

setup(
    name='SAMUS',
    version='1.0.0',
    description='SAMUS package',
    url='https://github.com/astertaylor/SAMUS',
    author='Aster Taylor',
    author_email='astertaylor@uchicago.edu',
    license="LICENSE",
    packages=['SAMUS'],
    install_requires=['numpy',
                      'numpy-quaternion',
                      'pandas',
                      'scipy',
                      'mpi4py',],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
    ],
    package_data={
        'SAMUS': ['meshes/*','examples/*','testing/*',
                  'examples/logs/*','testing/logs/*']},
    include_package_data=True,
    keywords = ["minor bodies", "fluid dynamics", "numerics", "asteroid",
    "comet", "tides", "tidal forces", "tidal deformation"],
    readme = "README.md",
    long_description_content_type='text/markdown',
    long_description=read_file('README.md')
)
