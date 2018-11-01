from setuptools import setup

setup(
    name='cerebro',
    version='0.1-dev',
    packages=['cerebro'],
    entry_points={
      'console_scripts': [
          'cerebro = cerebro.__main__.main'
      ]
    },
    url='',
    license='',
    author='Célian Garcia',
    author_email='celian.garcia1@gmail.com',
    description=''
)
