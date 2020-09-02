from setuptools import setup

setup(
    name='peppa',
    version='0.1.0',
    packages=[''],
    url='https://github.com/skhortiuk/peppa',
    license='MIT',
    author='Serhii Khortiuk',
    author_email='khortiukserhii@ukr.net',
    description='',
    install_requires=["autopep8"],
    entry_points={
        "console_scripts": [
            "peppa=peppa:main",
        ]
    },
)
