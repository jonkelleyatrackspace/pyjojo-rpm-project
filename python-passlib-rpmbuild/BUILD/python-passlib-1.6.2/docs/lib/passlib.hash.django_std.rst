.. index:: Django; hash formats

=============================================================
:samp:`passlib.hash.django_{digest}` - Django-specific Hashes
=============================================================

.. currentmodule:: passlib.hash

The `Django <http://www.djangoproject.com>`_ web framework
provides a module for storing user accounts and passwords
(:mod:`!django.contrib.auth`).
This module's password hashing code supports a few simple salted digests,
stored using the format :samp:`{id}${salt}${checksum}` (where :samp:`{id}`
is an identifier assigned by Django).
Passlib provides support for all the hashes used up to and including
Django 1.4

.. seealso::

    * :ref:`passlib.apps.django_context <django-contexts>` -
      a set of premade contexts which mimic Django's builtin hashing policy,
      and can read all of the formats listed below.

..
    * :mod:`passlib.ext.django` - a plugin that
      updates Django to use a stronger hashing scheme,
      and migrates existing hashes as users log in.

.. _django-1.4-hashes:

Django 1.4 Hashes
=================
Django 1.4 introduced a new "hashers" framework, as well as
three new modern large-salt variable-cost hash algorithms:

* :class:`django_pbkdf2_sha256` - a PBKDF2-HMAC-SHA256 based hash.
* :class:`django_pbkdf2_sha1` - a PBKDF2-HMAC-SHA1 based hash.
* :class:`django_bcrypt` - a wrapper around :class:`~passlib.hash.bcrypt`.

These classes can be used directly as follows::

    >>> from passlib.hash import django_pbkdf2_sha256 as handler

    >>> # encrypt password
    >>> h = handler.encrypt("password")
    >>> h
    'pbkdf2_sha256$10000$s1w0UXDd00XB$+4ORmyvVWAQvoAEWlDgN34vlaJx1ZTZpa1pCSRey2Yk='

    >>> # verify password
    >>> handler.verify("password", h)
    True
    >>> handler.verify("eville", h)
    False

.. seealso:: the generic :ref:`PasswordHash usage examples <password-hash-examples>`

Interface
---------

.. autoclass:: django_pbkdf2_sha256()
.. autoclass:: django_pbkdf2_sha1()
.. data:: django_bcrypt()

    This class implements Django 1.4's BCrypt wrapper, and follows the :ref:`password-hash-api`.

    This is identical to :class:`!bcrypt` itself, but with
    the Django-specific prefix ``"bcrypt$"`` prepended.
    See :doc:`/lib/passlib.hash.bcrypt` for more details,
    the usage and behavior is identical.

    This should be compatible with the hashes generated by
    Django 1.4's :class:`!BCryptPasswordHasher` class.

    .. versionadded:: 1.6

.. autoclass:: django_bcrypt_sha256()

Format
------
An example :class:`!django_pbkdf2_sha256` hash (of ``password``) is:

    ``pbkdf2_sha256$10000$s1w0UXDd00XB$+4ORmyvVWAQvoAEWlDgN34vlaJx1ZTZpa1pCSRey2Yk=``

Both of Django's PBKDF2 hashes have the same basic format,
:samp:`{ident}${rounds}${salt}${checksum}`, where:

* :samp:`{ident}` is an identifier (``pbkdf2_sha256`` in the case of the example).

* :samp:`{rounds}` is a variable cost parameter encoded in decimal.

* :samp:`{salt}` consists of (usually 12) alphanumeric digits
  (``s1w0UXDd00XB`` in the example).

* :samp:`{checksum}` is the base64 encoding the PBKDF2 digest.

The digest porition is generated by passing the ``utf-8`` encoded password,
the ``ascii``-encoded salt string, and the number of rounds into
PBKDF2 using the HMAC-SHA256 prf; and generated a 32 byte checksum,
which is then encoding using base64.

The other PBKDF2 wrapper functions similarly.

Django 1.0 Hashes
=================
.. warning::

    All of the following hashes are very susceptible to brute-force attacks;
    since they are simple single-round salted digests.
    They should not be used for any purpose
    besides manipulating existing Django password hashes.

Django 1.0 supports some basic salted digests, as well as some
legacy hashes:

* :class:`django_salted_sha1` - simple salted SHA1 digest, Django 1.0-1.3's default.
* :class:`django_salted_md5` - simple salted MD5 digest.
* :class:`django_des_crypt` - support for legacy :class:`des_crypt` hashes,
  shoehorned into Django's hash format.

These classes can be used directly as follows::

    >>> from passlib.hash import django_salted_sha1 as handler

    >>> # encrypt password
    >>> h = handler.encrypt("password")
    >>> h
    'sha1$c6218$161d1ac8ab38979c5a31cbaba4a67378e7e60845'

    >>> # verify password
    >>> handler.verify("password", h)
    True
    >>> handler.verify("eville", h)
    False

.. seealso:: the generic :ref:`PasswordHash usage examples <password-hash-examples>`

Interface
---------

.. autoclass:: django_salted_md5()
.. autoclass:: django_salted_sha1()

Format
------
An example :class:`!django_salted_sha1` hash (of ``password``) is:

    ``sha1$f8793$c4cd18eb02375a037885706d414d68d521ca18c7``

Both of Django's salted hashes have the same basic format,
:samp:`{ident}${salt}${checksum}`, where:

* :samp:`{ident}` is an identifier (``sha1`` in the case of the example,
  ``md5`` for :class:`!django_salted_md5`).

* :samp:`{salt}` consists of (usually 5) lowercase hexidecimal digits (``f8793`` in the example).

* :samp:`{checksum}` is lowercase hexidecimal encoding of the checksum.

The checksum is generated by concatenating the salt digits followed
by the password, and hashing them using the specified digest (MD5 or SHA-1).
The digest is then encoded to hexidecimal.
If the password is unicode, it is converted to ``utf-8`` first.

Security Issues
---------------
Django's salted hashes should not be considered very secure.

* They use only a single round of digests with known collision
  and pre-image attacks (SHA1 & MD5).

* While it could be increased, they currently use only 20 bits
  of entropy in their salt, which is borderline insufficient to defeat
  rainbow tables.

* They digest the encoded hexidecimal salt, not the raw bytes,
  increasing the odds that a particular salt+password string
  will be present in a pre-computed tables of ascii digests.

Des Crypt Wrapper
=================

.. autoclass:: django_des_crypt()

Format
------
An example :class:`!django_des_crypt` hash (of ``password``) is
``crypt$cd1a4$cdlRbNJGImptk``; the general format is the same
as the salted hashes: :samp:`{ident}${salt}${checksum}`, where:

* :samp:`{ident}` is the identifier ``crypt``.

* :samp:`{salt}` is 5 lowercase hexidecimal digits (``cd1a4`` in the example).

* :samp:`{checksum}` is a :class:`!des_crypt` hash (``cdlRbNJGImptk`` in the example).

It should be noted that this class essentially just shoe-horns
:class:`des_crypt` into a format compatible with the Django salted hashes (above).
It has a few quirks, such as the fact that only the first two characters
of the salt are used by :class:`!des_crypt`, and they are in turn
duplicated as the first two characters of the checksum.

For security issues relating to :class:`!django_des_crypt`,
see :class:`des_crypt`.

Other Hashes
============

.. autoclass:: django_disabled()

.. note::

    Some older (pre-1.0) versions of Django encoded
    passwords using :class:`~passlib.hash.hex_md5`,
    though this has been deprecated by Django,
    and should become increasingly rare.
