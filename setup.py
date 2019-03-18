from setuptools import setup

setup(
    name='cerebro',
    version='0.1-dev',
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
