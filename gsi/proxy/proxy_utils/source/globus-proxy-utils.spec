%ifarch alpha ia64 ppc64 s390x sparc64 x86_64
%global flavor gcc64
%else
%global flavor gcc32
%endif

Name:		globus-proxy-utils
%global _name %(tr - _ <<< %{name})
Version:	4.0
Release:	1%{?dist}
Summary:	Globus Toolkit - Globus GSI Proxy Utility Programs

Group:		Applications/Internet
License:	ASL 2.0
URL:		http://www.globus.org/
#		Source is extracted from the globus toolkit installer:
#		wget -N http://www-unix.globus.org/ftppub/gt5/5.0/5.0.2/installers/src/gt5.0.2-all-source-installer.tar.bz2
#		tar -jxf gt5.0.2-all-source-installer.tar.bz2
#		mv gt5.0.2-all-source-installer/source-trees/gsi/proxy/proxy_utils/source globus_proxy_utils-3.9
#		cp -p gt5.0.2-all-source-installer/source-trees/core/source/GLOBUS_LICENSE globus_proxy_utils-3.9
#		tar -zcf globus_proxy_utils-3.9.tar.gz globus_proxy_utils-3.9
Source:		%{_name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	openssl%{?_isa} >= 1
Requires:	globus-gsi-credential%{?_isa} >= 3
BuildRequires:	grid-packaging-tools
BuildRequires:	globus-gsi-proxy-ssl-devel%{?_isa} >= 1
BuildRequires:	globus-gsi-credential-devel%{?_isa} >= 3
BuildRequires:	globus-gsi-callback-devel%{?_isa}
BuildRequires:	globus-openssl-module-devel%{?_isa}
BuildRequires:	globus-gss-assist-devel%{?_isa} >= 3
BuildRequires:	globus-gsi-openssl-error-devel%{?_isa}
BuildRequires:	openssl-devel%{?_isa} >= 1
BuildRequires:	globus-gsi-proxy-core-devel%{?_isa} >= 1
BuildRequires:	globus-core%{?_isa} >= 4
BuildRequires:	globus-gsi-cert-utils-devel%{?_isa} >= 1
BuildRequires:	globus-common-devel%{?_isa} >= 3
BuildRequires:	globus-gsi-sysconfig-devel%{?_isa} >= 1

%description
The Globus Toolkit is an open source software toolkit used for building Grid
systems and applications. It is being developed by the Globus Alliance and
many others all over the world. A growing number of projects and companies are
using the Globus Toolkit to unlock the potential of grids for their cause.

The %{name} package contains:
Globus GSI Proxy Utility Programs

%prep
%setup -q -n %{_name}-%{version}

%build
# Remove files that should be replaced during bootstrap
rm -f doxygen/Doxyfile*
rm -f doxygen/Makefile.am
rm -f pkgdata/Makefile.am
rm -f globus_automake*
rm -rf autom4te.cache
unset GLOBUS_LOCATION
unset GPT_LOCATION

%{_datadir}/globus/globus-bootstrap.sh

%configure --with-flavor=%{flavor} --docdir=%{_docdir}/%{name}-%{version}

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

GLOBUSPACKAGEDIR=$RPM_BUILD_ROOT%{_datadir}/globus/packages


# Generate package filelists
cat $GLOBUSPACKAGEDIR/%{_name}/%{flavor}_pgm.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_doc.filelist \
    $GLOBUSPACKAGEDIR/%{_name}/noflavor_data.filelist \
  | sed -e s!^!%{_prefix}! -e 's!.*/man/.*!%doc &*!' > package.filelist

%clean
rm -rf $RPM_BUILD_ROOT

%files -f package.filelist
%defattr(-,root,root,-)
%dir %{_datadir}/globus/packages/%{_name}
%dir %{_docdir}/%{name}-%{version}

%changelog
* Sat Jul 17 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.9-1
- Update to Globus Toolkit 5.0.2
- Drop patch globus-proxy-utils-oid.patch (fixed upstream)

* Mon May 31 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.7-2
- Fix OID registration pollution

* Wed Apr 14 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.7-1
- Update to Globus Toolkit 5.0.1
- Drop patches globus-proxy-utils-ldflag-overwrt.patch and
  globus-proxy-utils-deps.patch (fixed upstream)

* Fri Jan 22 2010 Mattias Ellert <mattias.ellert@fysast.uu.se> - 3.5-1
- Update to Globus Toolkit 5.0.0

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.5-4
- rebuilt with new openssl

* Thu Jul 23 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.5-3
- Add instruction set architecture (isa) tags

* Wed Jun 03 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.5-2
- Update to official Fedora Globus packaging guidelines

* Thu Apr 16 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.5-1
- Make comment about source retrieval more explicit
- Change defines to globals
- Remove explicit requires on library packages
- Put GLOBUS_LICENSE file in extracted source tarball

* Sun Mar 15 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.5-0.5
- Adapting to updated globus-core package

* Thu Feb 26 2009 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.5-0.4
- Add s390x to the list of 64 bit platforms

* Tue Dec 30 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.5-0.3
- Adapt to updated GPT package

* Wed Oct 15 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.5-0.2
- Update to Globus Toolkit 4.2.1

* Mon Jul 14 2008 Mattias Ellert <mattias.ellert@fysast.uu.se> - 2.1-0.1
- Autogenerated
