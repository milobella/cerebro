from setuptools import setup

with open('VERSION.txt', 'r') as fp:
    version = fp.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    # == Name & descriptions ==
    name='cerebro',
    url='',
    license='',
    author='Célian Garcia',
    author_email='celian.garcia1@gmail.com',
    description='',

    # == Technical configuration ==
    version=version,
    require=requirements,
    setup_requires=["pytest-runner"],
    py_modules=['cerebro'],

)
