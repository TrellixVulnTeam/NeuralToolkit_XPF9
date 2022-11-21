from setuptools import find_packages, setup
setup(
    name='neuraltoolkit',
    packages=find_packages(include=['neuraltoolkit']),
    version='0.1.5',
    description='Toolkit for Neural Data Analyisis',
    author='izaquielcordeiro',
    license='MIT',
    install_requires=['pandas','numpy','klusta', 'matplotlib', 'plotly' \
                      ,'ipywidgets','IPython'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)