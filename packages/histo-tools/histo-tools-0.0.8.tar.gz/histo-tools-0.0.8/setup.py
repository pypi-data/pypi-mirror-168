from setuptools import find_packages, setup
setup(
    name='histo-tools',
    version='0.0.8',
    description='General histology tools.',
    author='Austin E. Y. T. Lefebvre',
    license='MIT',
    author_email='austin.e.lefebvre@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/aelefebv/histo-tools',
    keywords='histology',
    install_requires=[
        'numpy',
        'zarr',
        'imagecodecs',
        'tifffile',
      ],
)
