from setuptools import find_packages, setup
setup(
    name='dial-clean',
    packages=find_packages(include=['dial_clean']),
    package_data = {
        'dial_clean': ['tool_data/*']
    },
    version='0.1.1',
    description='My first Python library',
    author='songyi',
    author_email='757503218@qq.com',
    url='https://github.com/everks/dial-clean',
    install_requires=['numpy==1.19.5', 'hanziconv==0.3.2', 'zhon==1.1.5'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.0.1'],
    test_suite='tests',
    entry_points={
        'console_scripts':[
            'dial-clean = dial_clean.main:main'
        ]
    }
)