#
# This is currently not suitable for Fedora, as llvm is compiled with additional patches
# This is planned to change in future, when the llvm patches are upstreamed
#
# Issues
# - [ ] Custom LLVM
# - [ ] Hardcoded libdir
# - [ ] 0.6 is unreleased
# - [ ] x86_64 only (not handled)
#

Name:           rust
Version:        0.6
Release:        1%{?dist}
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


%filter_from_requires /x86_64-unknown-linux-gnu/d
%filter_requires_in -P bin/(rust|cargo).*
%filter_setup

%description
This is a compiler for Rust, including standard libraries, tools and
documentation.


%prep
%setup -q

# Prevent cusotm configure from failing
sed -i "/^.*is not recog.*/ s/.*/echo configure: Argument \"'\$arg'\" is not recognized and ignored./" configure

# Remove rpaths
sed -i "/get_rpath_flags/d" src/librustc/back/link.rs


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
EOF


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
%{_bindir}/cargo*
%{_prefix}/lib/libcargo*


%changelog
* Fri Mar 01 2013 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.6-1
- Initial package
