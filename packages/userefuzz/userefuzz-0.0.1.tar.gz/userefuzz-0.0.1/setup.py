from setuptools import setup

setup(
    name='userefuzz',
    version='0.0.1',    
    description='User-Agent and Referer Header SQLI Fuzzer',
    url='https://twitter.com/root_tanishq',
    author='Tanishq Rathore',
    license='MIT',
    packages=['userefuzz'],
    scripts=['userefuzz/userefuzz'],
    install_requires=['requests==2.28.1'],

    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)

