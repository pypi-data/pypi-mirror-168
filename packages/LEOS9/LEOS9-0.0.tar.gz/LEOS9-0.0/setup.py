from setuptools import setup, find_packages

setup(
    name='LEOS9',
    version='0.0',
    license='FGI',
    author="Fabricio Prol",
    author_email='fabricioprol@hotmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/fabprol/LEO-S9/src',
    keywords='LEO',
    install_requires=[
          'scikit-learn',
      ],

)