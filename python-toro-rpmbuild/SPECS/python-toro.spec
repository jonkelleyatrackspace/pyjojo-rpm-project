%define name toro
%define version 0.5
%define unmangled_version 0.5
%define unmangled_version 0.5
%define release 1

Summary: Synchronization primitives for Tornado coroutines.
Name: python-%{name}
Requires: python-tornado >= 4.0.2
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: http://www.apache.org/licenses/LICENSE-2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: A. Jesse Jiryu Davis <ajdavis@cs.oberlin.edu>
Url: http://github.com/ajdavis/toro/

%description
====
toro
====

.. image:: https://raw.github.com/ajdavis/toro/master/doc/_static/toro.png

:Info: Synchronization primitives for Tornado coroutines.
:Author: A\. Jesse Jiryu Davis

Documentation: http://toro.readthedocs.org/

.. image:: https://travis-ci.org/ajdavis/toro.png
        :target: https://travis-ci.org/ajdavis/toro

About
=====
A set of locking and synchronizing primitives analogous to those in Python's
`threading module`_ or Gevent's `coros`_, for use with Tornado's `gen.engine`_.

.. _threading module: http://docs.python.org/library/threading.html

.. _coros: http://www.gevent.org/gevent.coros.html

.. _gen.engine: http://www.tornadoweb.org/documentation/gen.html

Dependencies
============
Tornado_ >= version 2.3.

.. _Tornado: http://www.tornadoweb.org/

Examples
========
Here's a basic example (for more see the *examples* section of the docs):

.. code-block:: python

    from tornado import ioloop, gen
    import toro

    q = toro.JoinableQueue(maxsize=3)

    @gen.coroutine
    def consumer():
        while True:
            item = yield q.get()
            try:
                print 'Doing work on', item
            finally:
                q.task_done()

    @gen.coroutine
    def producer():
        for item in range(10):
            yield q.put(item)

    producer()
    consumer()
    loop = ioloop.IOLoop.instance()
    # block until all tasks are done
    q.join().add_done_callback(loop.stop)
    loop.start()

Documentation
=============

You will need Sphinx_ and GraphViz_ installed to generate the
documentation. Documentation can be generated like:

.. code-block:: console

    $ sphinx-build doc build

.. _Sphinx: http://sphinx.pocoo.org/

.. _GraphViz: http://www.graphviz.org/

Testing
=======

Run ``python setup.py nosetests`` in the root directory.

Toro boasts 100% code coverage, including branch-coverage!


%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
