from setuptools import setup, find_packages


setup(
    name='netcdf-modifier',
    version='0.1',
    license='MIT',
    author="Utpal Singh",
    author_email='utpal_singh@yahoo.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/utpal-singh/netcdf-modifier',
    keywords='netcdf',
    install_requires=[
          'numpy', 'netCDF4'
      ],

)
