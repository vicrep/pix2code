from setuptools import find_packages
from setuptools import setup

REQUIREMENTS = [
    'keras',
    'numpy',
    'opencv-python',
    'h5py'
]

setup(
    name='pix2code',
    install_requires=REQUIREMENTS,
    packages=find_packages(),
    include_package_data=True,
    description='Pix2Code'
)
