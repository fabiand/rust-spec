%global commit a33d046b2491adfe05655bc252037ab260f9c485
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate 20150428
%global gitversion .git%{commitdate}.%{shortcommit}
%global source https://github.com/llvm-mirror/%{name}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

Name:           compiler-rt
Version:        0.1
Release:        1%{?dist}
Summary:        Common compiler runtime libraries

License:        MIT, NCSA
URL:            http://compiler-rt.llvm.org/
Source0:        %{source}

BuildRequires:  make
BuildRequires:  git
BuildRequires:  clang

ExclusiveArch:  x86_64


%description
A simple library that provides an implementation of the low-level target-specific hooks required by code generation and other runtime components.


%package static
Summary:        Static common compiler runtime libraries


%description static
A simple library that provides an implementation of the low-level target-specific hooks required by code generation and other runtime components.


%prep
%setup -qn %{name}-%{?commit}


%build
make %{?_smp_mflags} clang_linux


%install
mkdir -p %{buildroot}%{_libdir}/
cp -v clang_linux/builtins-x86_64/libcompiler_rt.a \
      %{buildroot}%{_libdir}/


%files static
%license LICENSE.TXT
%doc CODE_OWNERS.TXT CREDITS.TXT README.txt
%{_libdir}/libcompiler_rt.a


%changelog
* Tue Apr 28 2015 Fabian Deutsch <fabiand@fedoraproject.org> - 0.1-0.1.git20150428.a33d046
- Initial package
