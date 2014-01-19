#
# TODO:
#	- provide the dependencies for optional features (the BuildRequires
#	  currently commented-out)

# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Open Vulnerability Assessment System libraries
Name:		openvas-libraries
Version:	6.0.1
Release:	0.1
# this license that apply to the whole package see COPYING for more information
License:	GPL v2
Group:		Libraries
Source0:	http://wald.intevation.org/frs/download.php/1417/%{name}-%{version}.tar.gz
# Source0-md5:	ece48f91998597d4ad700ce3fb1d5fa3
Patch0:		link_gpgme.patch
URL:		http://www.openvas.org/
BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	flex
BuildRequires:	glib2-devel >= 2.16
BuildRequires:	gnutls-devel >= 2.8
BuildRequires:	gpgme-devel
BuildRequires:	libksba-devel
BuildRequires:	libpcap-devel
BuildRequires:	libssh-devel
BuildRequires:	libuuid-devel
BuildRequires:	openldap-devel
BuildRequires:	pkgconfig
#BuildRequires:	wmiclient
%if %{with apidocs}
BuildRequires:	doxygen
#BuildRequires:	sqlfairy
#BuildRequires:	xmltoman
%endif
BuildRequires:	rpmbuild(macros) >= 1.583
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# dependency loop between libopenvas_misc and libopenvas_nasl
# Unresolved symbols found in: .../libopenvas_misc.so.6.0.1
#	nasl_ssh_internal_close
%define		skip_post_check_so	libopenvas_misc.so.*

%description
This is the libraries module for the Open Vulnerability Assessment
System (OpenVAS).

The Open Vulnerability Assessment System (OpenVAS) is a framework of
several services and tools offering a comprehensive and powerful
vulnerability scanning and vulnerability management solution.

%package -n openvas-common
Summary:	Common files for Open Vulnerability Assessment System
Summary(pl.UTF-8):	Wspólne pliki OpenVAS
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n openvas-common
Common files for Open Vulnerability Assessment System.

%description -n openvas-common -l pl.UTF-8
Wspólne pliki OpenVAS.

%package devel
Summary:	Header files for OpenVAS libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek OpenVAS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for OpenVAS libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek OpenVAS.

%package static
Summary:	Static OpenVAS libraries
Summary(pl.UTF-8):	Statyczna biblioteki OpenVAS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenVAS libraries.

%description static -l pl.UTF-8
Statyczna biblioteka OpenVAS.

%package apidocs
Summary:	OpenVAS API documentation
Summary(pl.UTF-8):	Dokumentacja API bibliotek OpenVAS
Group:		Documentation

%description apidocs
OpenVAS API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek OpenVAS.

%prep
%setup -q

%patch0 -p1

%build
install -d build
cd build
%cmake \
	-DLOCALSTATEDIR=/var \
	..
%{__make}

%if %{with apidocs}
%{__make} doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README COPYING CHANGES ChangeLog
%doc doc/example.*
%attr(755,root,root) %{_libdir}/libopenvas*.so.6.*.*
%attr(755,root,root) %ghost %{_libdir}/libopenvas*.so.6

%files -n openvas-common
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/openvas-nasl
%dir %{_sysconfdir}/openvas
%dir %{_datadir}/openvas
%{_datadir}/openvas/openvas-services
%attr(755,root,root) %{_datadir}/openvas/openvas-lsc-rpm-creator.sh
%dir /var/cache/openvas
%dir /var/lib/openvas
%dir /var/lib/openvas/plugins
%dir /var/lib/openvas/users
%dir /var/log/openvas
%{_mandir}/man1/openvas-nasl.1*

%files devel
%defattr(644,root,root,755)
%doc doc/signatures-howto.txt
%attr(755,root,root) %{_libdir}/libopenvas*.so
%{_includedir}/openvas
%{_pkgconfigdir}/libopenvas.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libopenvas*.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/generated/html/*
%endif
