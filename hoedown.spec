Name:           hoedown
Version:        3.0.3
Release:        1%{?dist}
Summary:        Standards compliant, fast, secure markdown processing library in C

License:        MIT
URL:            https://github.com/hoedown/hoedown
Source0:        https://github.com/%{name}/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  gcc


%description
Hoedown is a revived fork of Sundown, the Markdown parser based on the original code of the Upskirt library by Natacha Porté.

%package static
Summary:        Static standards compliant, fast, secure markdown processing library in C


%description static
TBD


%package devel
Summary:        Devel files


%description devel
TBD


%prep
%setup -q


%build
make %{?_smp_mflags} CFLAGS="%{optflags}" LDFLAGS="%{__global_ldflags}" all


%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix} \
      BINDIR=%{_bindir} LIBDIR=%{_libdir} INCLUDEDIR=%{_includedir}

%files
%license LICENSE
%doc README.md
%{_bindir}/hoedown
%{_bindir}/smartypants
%{_libdir}/libhoedown.so.3


%files static
%{_libdir}/libhoedown.a


%files devel
%{_libdir}/libhoedown.so
%{_includedir}/hoedown



%changelog
* Tue May 26 2015 Josh Stone <jistone@redhat.com> - 3.0.3-1
- Update to 3.0.3

* Tue Apr 28 2015 Fabian Deutsch <fabiand@fedoraproject.org> - 3.0.2-1
- Initial package
