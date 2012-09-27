from setuptools import setup, find_packages

version = '1.0'

setup(name='pygments-openssl',
      version=version,
      description='Pygments lexer for OpenSSL configuration files',
      long_description=open('README.txt').read() + '\n' +
                       open('CHANGES.txt').read(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Plugins',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          #'Programming Language :: Python :: 3',
      ],
      keywords='pygments openssl conf lexer openssl.cnf openssl.conf',
      author='Stefan H. Holek',
      author_email='stefan@epy.co.at',
      url='http://pypi.python.org/pypi/pygments-openssl',
      license='BSD',
      py_modules=['lexer'],
      #include_package_data=True,
      zip_safe=True,
      #use_2to3=True,
      #test_suite='opensslconflexer.tests',
      #tests_require=[
      #    'flexmock',
      #],
      install_requires=[
          'setuptools',
      ],
      entry_points={
          'pygments.lexers': 'openssl=lexer:OpenSSLConfLexer',
      },
)
