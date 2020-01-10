%global shortname srtp
%global cvsver 20101004cvs

Name:		lib%{shortname}
Version:	1.4.4
Release:	9.%{cvsver}%{?dist}
Summary:	An implementation of the Secure Real-time Transport Protocol (SRTP)
Group:		System Environment/Libraries
License:	BSD
URL:		http://srtp.sourceforge.net
# Upstream 1.4.4 tarball is a bit dated, need to use cvs
# cvs -d:pserver:anonymous@srtp.cvs.sourceforge.net:/cvsroot/srtp co -P srtp
# tar cvfj srtp-1.4.4-20101004cvs.tar.bz2 srtp/
Source0:	%{shortname}-%{version}-%{cvsver}.tar.bz2
# Pkgconfig goodness
Source1:	libsrtp.pc
# Universal config.h
Source2:	config.h

# Seriously. Who doesn't do shared libs these days?
# And how does Chromium always manage to find these projects and use them?
Patch0:		libsrtp-1.4.4-shared.patch

%description
This package provides an implementation of the Secure Real-time
Transport Protocol (SRTP), the Universal Security Transform (UST), and
a supporting cryptographic kernel. 

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{shortname}
%patch0 -p1 -b .shared

# Fix end-of-line encoding
sed -i 's/\r//g' doc/draft-irtf-cfrg-icm-00.txt

%if 0%{?rhel} > 0
%ifarch ppc64
sed -i 's/-z noexecstack//' Makefile.in
%endif
%endif

%build
export CFLAGS="%{optflags} -fPIC"
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'
pushd %{buildroot}%{_libdir}
ln -sf libsrtp.so.0.0.0 libsrtp.so
ln -sf libsrtp.so.0.0.0 libsrtp.so.0
popd

# Install the pkg-config file
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
install -m0644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/
# Fill in the variables
sed -i "s|@PREFIX@|%{_prefix}|g" %{buildroot}%{_libdir}/pkgconfig/libsrtp.pc
sed -i "s|@LIBDIR@|%{_libdir}|g" %{buildroot}%{_libdir}/pkgconfig/libsrtp.pc
sed -i "s|@INCLUDEDIR@|%{_includedir}|g" %{buildroot}%{_libdir}/pkgconfig/libsrtp.pc

# Handle multilib issues with config.h
mv %{buildroot}%{_includedir}/%{shortname}/config.h %{buildroot}%{_includedir}/%{shortname}/config-%{__isa_bits}.h
cp -a %{SOURCE2} %{buildroot}%{_includedir}/%{shortname}/config.h

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE README TODO VERSION doc/*.txt doc/*.pdf
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{shortname}/
%{_libdir}/pkgconfig/libsrtp.pc
%{_libdir}/*.so

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.4.4-9.20101004cvs
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.4.4-8.20101004cvs
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-7.20101004cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 25 2012 Karsten Hopp <karsten@redhat.com> 1.4.4-6.20101004cvs
- use __PPC64__, not __ppc64__ which is undefined on PPC64 arch

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-5.20101004cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 21 2012 Tom Callaway <spot@fedoraproject.org> - 1.4.4-4.20101004cvs
- handle config.h multilib (bz787537)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-3.20101004cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-2.20101004cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Jeffrey C. Ollie <jeff@ocjtech.us>
- Don't use '-z noexecstack' option for linker on PPC64 (EL6)

* Mon Oct  4 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4.4-1.20101004cvs
- initial package
