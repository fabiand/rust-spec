#
# This is currently not suitable for Fedora, as llvm is compiled with additional patches
# This is planned to change in future, when the llvm patches are upstreamed
#
# Issues
# - Custom LLVM - use --llvm-root=?
# - Hardcoded libdir
# - libuv is included
#
# Wiki page: https://github.com/mozilla/rust/wiki/Note-packaging
#

Name:           rust
Version:        0.6
Release:        2%{?dist}
Summary:        The Rust Programming Language

License:        ASL 2.0, MIT
URL:            http://www.rust-lang.org
Source0:        http://static.rust-lang.org/dist/%{name}-%{version}.tar.gz

BuildRequires:  llvm-devel
BuildRequires:  clang-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  python
BuildRequires:  perl
BuildRequires:  curl
#BuildRequires:  pandoc
BuildRequires:  chrpath

# LLVM features are only present in x86_64
BuildArch:      x86_64

%filter_from_requires /x86_64-unknown-linux-gnu/d
%filter_requires_in -P bin/(rust|cargo).*
%filter_setup

%description
This is a compiler for Rust, including standard libraries, tools and
documentation.


%prep
%setup -q

# Prevent custom configure from failing
sed -i "/^.*is not recog.*/ s/.*/echo configure: Argument \"'\$arg'\" is not recognized and ignored./" configure


%build
%configure

# LD_LIBRARY_PATH is passed to tell the linker were to find the different libraries,
# this is needed because the rpaths were removed in prep
make %{?_smp_mflags} \
	LD_LIBRARY_PATH=x86_64-unknown-linux-gnu/stage0/lib/:x86_64-unknown-linux-gnu/stage1/lib/:x86_64-unknown-linux-gnu/stage2/lib/:x86_64-unknown-linux-gnu/stage3/lib/ 


%install
make install DESTDIR=%{buildroot}

#mv %{buildroot}/%{_prefix}/lib %{buildroot}/%{_libdir}

# Create ld.so.conf file
mkdir -p %{buildroot}/%{_sysconfdir}/ld.so.conf.d
cat <<EOF >/%{buildroot}/%{_sysconfdir}/ld.so.conf.d/rust-%{_arch}.conf
%{_prefix}/lib/rustc/
%{_prefix}/lib/rustc/x86_64-unknown-linux-gnu/lib/
EOF

# Remove rpaths
{ find %{buildroot}/usr/bin -type f ; find %{buildroot} -type f -name \*.so ; } | xargs chrpath --delete

%post -p /sbin/ldconfig


%files
%doc COPYRIGHT LICENSE-APACHE LICENSE-MIT README.md
%{_sysconfdir}/ld.so.conf.d/rust-%{_arch}.conf
%{_bindir}/rust*
%{_prefix}/lib/librust*
%{_prefix}/lib/libstd*
%{_prefix}/lib/libcore*
%{_prefix}/lib/libsyntax*
%{_prefix}/lib/rustc/*
%{_datadir}/man/*


%changelog
* Fri Apr 19 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 0.6-2
- Update to rust-0.6
- Remove cargo
- Fix rpath issues differently (chrpath)

* Fri Mar 01 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 0.6-1
- Initial package
