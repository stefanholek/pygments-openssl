from setuptools import setup, find_packages

version = '1.5'

setup(name='pygments-openssl',
      version=version,
      description='Syntax coloring for OpenSSL configuration files',
      long_description=open('README.rst').read() + '\n' +
                       open('CHANGES.rst').read(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Plugins',
          'Intended Audience :: Developers',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Text Processing :: Filters',
      ],
      keywords='sphinx pygments openssl conf lexer openssl.cnf',
      author='Stefan H. Holek',
      author_email='stefan@epy.co.at',
      url='https://github.com/stefanholek/pygments-openssl',
      license='BSD-2-Clause',
      packages=find_packages(),
      install_requires=[
          'setuptools',
          'pygments',
      ],
      entry_points={
          'pygments.lexers': 'openssl=pygments_openssl.lexer:OpenSSLConfLexer',
      },
      python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
)
