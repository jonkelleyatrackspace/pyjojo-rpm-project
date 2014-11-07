%define name pyjojo
%define version 0.9
%define unmangled_version 0.9
%define unmangled_version 0.9
%define release 1

Summary: Expose a set of shell scripts as an API.
Name: %{name}
Requires: python-backports-ssl_match_hostname >= 3.4.0.2, python-setuptools >= 0.6, PyYAML%{?_isa} >= 3.10, python-toro >= 0.5, python-tornado >= 3.0.1, python-passlib >= 1.6
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: UNKNOWN
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Anthony Tarola <anthony.tarola@gmail.com>
Url: https://github.com/atarola/pyjojo

%description
UNKNOWN

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
