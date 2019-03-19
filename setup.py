from setuptools import setup

version = None
with open('VERSION.txt', 'r') as fp:
    version = fp.read()

setup(
    name='cerebro',
    version=version,
    entry_points={
      'console_scripts': [
          'cerebro = cerebro:main'
      ]
    },
    py_modules=['cerebro'],
    url='',
    license='',
    author='Célian Garcia',
    author_email='celian.garcia1@gmail.com',
    description=''
)
