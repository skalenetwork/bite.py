from setuptools import find_packages, setup

setup(
    name='t-encrypt',
    version='0.0.1',
    packages=find_packages(),
    package_data={
        't_encrypt': ['*.so', '*.so.*'],
    },
    include_package_data=True,
    author='SKALE Labs',
    description='T-Encrypt library for threshold encryption',
    python_requires='>=3.10',
)
