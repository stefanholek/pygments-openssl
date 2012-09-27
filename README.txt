================
pygments-openssl
================
------------------------------------------------
A Pygments lexer for OpenSSL configuration files
------------------------------------------------

Overview
========

This package provides an OpenSSL_ configuration file lexer for Pygments_.
The lexer is published as an entry point and, once installed, Pygments will
pick it up automatically.

You can then use the ``openssl`` language with Pygments::

    $ pygmentize -l openssl /etc/openssl/openssl.cnf

.. _OpenSSL: http://openssl.org/
.. _Pygments: http://pygments.org/

Installation
============

Use your favorite installer to install pygments-openssl into the same
Python you have installed Pygments. For example::

    $ easy_install pygments-openssl

To verify the installation run::

    $ pygmentize -L lexer | grep -i openssl
    * openssl:
        OpenSSL (filenames *.cnf, *.conf)

