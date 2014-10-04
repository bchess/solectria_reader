from distutils.core import setup

setup(
    name='solectria-reader',
    version='0.1',
    author='Ben Chess',
    packages=['solectria-reader'],
    install_requires=['pySerial', 'crcmod']
)

