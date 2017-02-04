================
pygments-openssl
================
------------------------------------------------
Syntax coloring for OpenSSL configuration files
------------------------------------------------

Overview
========

This package provides a Pygments_ lexer for OpenSSL_ configuration files.
The lexer is published as an entry point and Pygments will pick it up
automatically.

You can use the ``openssl`` language with Pygments::

    $ pygmentize -l openssl /etc/openssl/openssl.cnf

In Sphinx_ documents the lexer is selected with the ``highlight`` directive::

    .. highlight:: openssl

.. _OpenSSL: https://www.openssl.org/docs/man1.1.0/apps/config.html
.. _Pygments: http://pygments.org/
.. _Sphinx: http://sphinx-doc.org/

Installation
============

Use your favorite installer to install pygments-openssl into the same
Python enviroment you have installed Pygments. For example::

    $ pip install pygments-openssl

To verify the installation run::

    $ pygmentize -L lexer | grep -i openssl
    * openssl:
        OpenSSL (filenames *.cnf, *.conf)

