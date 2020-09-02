from setuptools import setup

setup(
    name='peppa8',
    version='0.1.1',
    packages=[''],
    url='https://github.com/skhortiuk/peppa8',
    license='MIT',
    author='Serhii Khortiuk',
    author_email='khortiukserhii@ukr.net',
    description='',
    install_requires=["autopep8"],
    entry_points={
        "console_scripts": [
            "peppa8=peppa8:main",
        ]
    },
)
