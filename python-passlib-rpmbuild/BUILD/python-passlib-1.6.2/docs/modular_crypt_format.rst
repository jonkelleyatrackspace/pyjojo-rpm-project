.. index:: modular crypt format

.. _modular-crypt-format:

.. rst-class:: html-toggle

====================
Modular Crypt Format
====================

.. centered:: *or*, a side note about a standard that isn't

In short, the modular crypt format (MCF) is a standard
for encoding password hash strings, which requires hashes
have the format :samp:`${identifier}${content}`; where
:samp:`{identifier}` is an short alphanumeric string uniquely
identifying a particular scheme, and :samp:`{content}`
is the contents of the scheme, using only the characters
in the regexp range ``[a-zA-Z0-9./]``.

However, there appears to be no central registry of identifiers,
no specification document, and no actual rules;
so the modular crypt format is more of an ad-hoc idea rather than a true standard.

History
=======
Historically, most unix systems supported only :class:`~passlib.hash.des_crypt`.
Around the same time, many incompatible variations were also developed,
but their hashes were not easily distingiushable from each other
(see :ref:`archaic-unix-schemes`); making it impossible to use
multiple hashes on one system, or progressively migrate to a newer scheme.

This was solved with the advent of the MCF,
which was introduced around the time that :class:`~passlib.hash.md5_crypt` was developed.
This format allows hashes from multiple schemes to exist within the same
database, by requiring that all hash strings begin with a unique prefix
using the format :samp:`${identifier}$`.

Requirements
============
Unfortunately, there is no specification document for this format.
Instead, it exists in *de facto* form only; the following
is an attempt to roughly identify the conventions followed
by the modular crypt format hashes found in Passlib:

1. Hash strings should use only 7-bit ascii characters.

   No known OS or application generates hashes which violate this rule.
   However, some systems (e.g. Linux) will happily
   accept hashes which contain 8-bit characters in their salt,
   This is probably a case of "permissive in what you accept,
   strict in what you generate".

2. Hash strings should start with the prefix :samp:`${identifier}$`,
   where :samp:`{identifier}` is a short string uniquely identifying
   hashes generated by that algorithm, using only lower case ascii
   letters, numbers, and hyphens
   (c.f. the list of :ref:`known identifiers <mcf-identifiers>` below).

   When MCF was first introduced, most schemes choose a single digit
   as their identifier (e.g. ``$1$`` for :class:`~passlib.hash.md5_crypt`).
   Because of this, some older systems only look at the first
   character when attempting to distinguish hashes.
   However, as Unix variants have branched off,
   new schemes were developed which used larger
   identifying strings (e.g. ``$sha1$`` for :class:`~passlib.hash.sha1_crypt`).

   At this point, any new hash schemes should probably use a 6-8 character
   descriptive identifier, to avoid potential namespace clashes.

3. Hashes should only contain the ascii letters ``a``-``z`` and ``A``-``Z``,
   ascii numbers 0-9, and the characters ``./``; though additionally
   they may use the ``$`` character as an internal field separator.

   This is the least adhered-to of any modular crypt format convention.
   Other characters (such as ``=,-``) are sometimes
   used by various formats, though sparingly.

   The only hard and fast stricture
   is that ``:;!*`` and all non-printable characters be avoided,
   since this would interfere with parsing of the Unix shadow password file,
   where these hashes are typically stored.

   Pretty much all modular-crypt-format hashes
   use ascii letters, numbers, ``.``, and ``/``
   to provide base64 encoding of their raw data,
   though the exact character value assignments vary between hashes
   (see :data:`passlib.utils.h64`).

4. Hash schemes should put their "digest" portion
   at the end of the hash, preferably separated
   by a ``$``.

   This allows password hashes to be easily truncated
   to a "configuration string" containing just
   the identifying prefix, rounds, salt, etc.

   This configuration string then encodes all the information
   generated needed to generate a new hash
   in order to verify a password, without
   having to perform excessive parsing.

   Most modular crypt format hashes follow this convention,
   though some (like :class:`~passlib.hash.bcrypt`) omit the ``$`` separator
   between the configuration and the digest.

   Furthermore, there is no set standard about whether configuration
   strings should or should not include a trailing ``$`` at the end,
   though the general rule is that hashing should behave the same in either case
   (:class:`~passlib.hash.sun_md5_crypt` behaves particularly poorly
   regarding this last point).

.. note::

    All of the above is guesswork based on examination of existing
    hashes and OS implementations; and was written merely
    to clarify the issue of what the "modular crypt format" is.
    It is drawn from no authoritative sources.

.. index:: modular crypt format; known identifiers

.. _mcf-identifiers:

Identifiers & Platform Support
==============================

OS Defined Hashes
-----------------
The following table lists of all the major MCF hashes supported by Passlib,
and indicates which operating systems offer native support:

.. table::
    :column-alignment: llccccc
    :column-wrapping: nn

    ==================================== ==================== =========== =========== =========== =========== =======
    Scheme                               Prefix               Linux       FreeBSD     NetBSD      OpenBSD     Solaris
    ==================================== ==================== =========== =========== =========== =========== =======
    :class:`~passlib.hash.des_crypt`                          y           y           y           y           y
    :class:`~passlib.hash.bsdi_crypt`    ``_``                            y           y           y
    :class:`~passlib.hash.md5_crypt`     ``$1$``              y           y           y           y           y
    :class:`~passlib.hash.bcrypt`        ``$2$``, ``$2a$``,
                                         ``$2x$``, ``$2y$``               y           y           y           y
    :class:`~passlib.hash.bsd_nthash`    ``$3$``                          y
    :class:`~passlib.hash.sha256_crypt`  ``$5$``              y           8.3+                                y
    :class:`~passlib.hash.sha512_crypt`  ``$6$``              y           8.3+                                y
    :class:`~passlib.hash.sun_md5_crypt` ``$md5$``, ``$md5,``                                                 y
    :class:`~passlib.hash.sha1_crypt`    ``$sha1$``                                   y
    ==================================== ==================== =========== =========== =========== =========== =======

Additional Platforms
--------------------
The modular crypt format is also supported to some degree
by the following operating systems and platforms:

.. rst-class:: plain

===================== ==============================================================
**MacOS X**           Darwin's native :func:`!crypt` provides limited functionality,
                      supporting only :class:`~passlib.hash.des_crypt` and
                      :class:`~passlib.hash.bsdi_crypt`. OS X uses a separate
                      system for it's own password hashes.

**Google App Engine** As of 2011-08-19, Google App Engine's :func:`!crypt`
                      implementation appears to match that of a typical Linux
                      system.
===================== ==============================================================

Application-Defined Hashes
--------------------------
The following table lists the other MCF hashes supported by Passlib.
These hashes can be found in various libraries and applications
(and are not natively supported by any known OS):

.. table::
    :class: fullwidth
    :widths: 1 1 2
    :column-wrapping: nn

    =========================================== =================== ===========================
    Scheme                                      Prefix              Primary Use (if known)
    =========================================== =================== ===========================
    :class:`~passlib.hash.apr_md5_crypt`        ``$apr1$``          Apache htdigest files
    :class:`~passlib.hash.bcrypt_sha256`        ``$bcrypt-sha256$`` Passlib-specific
    :class:`~passlib.hash.phpass`               ``$P$``, ``$H$``    PHPass-based applications
    :class:`~passlib.hash.pbkdf2_sha1`          ``$pbkdf2$``        Passlib-specific
    :class:`~passlib.hash.pbkdf2_sha256`        ``$pbkdf2-sha256$`` Passlib-specific
    :class:`~passlib.hash.pbkdf2_sha512`        ``$pbkdf2-sha512$`` Passlib-specific
    :class:`~passlib.hash.scram`                ``$scram$``         Passlib-specific
    :class:`~passlib.hash.cta_pbkdf2_sha1`      ``$p5k2$`` [#cta]_
    :class:`~passlib.hash.dlitz_pbkdf2_sha1`    ``$p5k2$`` [#cta]_
    =========================================== =================== ===========================

.. rubric:: Footnotes

.. [#cta] :class:`!cta_pbkdf2_sha1` and :class:`!dlitz_pbkdf2_sha1` both use
          the same identifier. While there are other internal differences,
          the two can be quickly distinguished
          by the fact that cta hashes always end in ``=``, while dlitz
          hashes contain no ``=`` at all.
