from setuptools import setup, find_packages

version = '1.4'

setup(name='pygments-openssl',
      version=version,
      description='Syntax coloring for OpenSSL configuration files',
      long_description=open('README.rst').read() + '\n' +
                       open('CHANGES.rst').read(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Plugins',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      keywords='sphinx pygments openssl conf lexer openssl.cnf',
      author='Stefan H. Holek',
      author_email='stefan@epy.co.at',
      url='https://github.com/stefanholek/pygments-openssl',
      license='BSD-2-Clause',
      py_modules=['lexer'],
      packages=find_packages(),
      zip_safe=True,
      test_suite='tests',
      install_requires=[
          'setuptools',
          'pygments',
      ],
      entry_points={
          'pygments.lexers': 'openssl=lexer:OpenSSLConfLexer',
      },
)
