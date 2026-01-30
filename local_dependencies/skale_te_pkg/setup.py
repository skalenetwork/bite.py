from setuptools import find_packages, setup

setup(
    name='skale_te',
    version='0.0.1',
    description='SKALE Threshold Encryption Python bindings',
    packages=find_packages(),
    package_data={
        'skale_te': ['*.so'],
    },
    include_package_data=True,
)
