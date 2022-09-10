from setuptools import find_packages, setup
setup(
    name='neuraltoolkit',
    packages=find_packages(include=['neuraltoolkit']),
    version='0.0.2',
    description='My first Python library',
    author='Me',
    license='MIT',
    install_requires=['pandas','numpy','klusta', 'matplotlib'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)