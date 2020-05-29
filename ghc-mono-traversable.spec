#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	mono-traversable
Summary:	Type classes for mapping, folding, and traversing monomorphic containers
Name:		ghc-%{pkgname}
Version:	1.0.15.1
Release:	1
License:	MIT
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/mono-traversable
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	b321689d333f9c61c9350dcb813ba6fc
URL:		http://hackage.haskell.org/package/mono-traversable
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4.10
BuildRequires:	ghc-bytestring >= 0.9
BuildRequires:	ghc-containers >= 0.5.8
BuildRequires:	ghc-hashable
BuildRequires:	ghc-split >= 0.2
BuildRequires:	ghc-text >= 0.11
BuildRequires:	ghc-transformers >= 0.3
BuildRequires:	ghc-unordered-containers >= 0.2
BuildRequires:	ghc-vector >= 0.10
BuildRequires:	ghc-vector-algorithms >= 0.6
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-base-prof >= 4.10
BuildRequires:	ghc-bytestring-prof >= 0.9
BuildRequires:	ghc-containers-prof >= 0.5.8
BuildRequires:	ghc-hashable-prof
BuildRequires:	ghc-split-prof >= 0.2
BuildRequires:	ghc-text-prof >= 0.11
BuildRequires:	ghc-transformers-prof >= 0.3
BuildRequires:	ghc-unordered-containers-prof >= 0.2
BuildRequires:	ghc-vector-prof >= 0.10
BuildRequires:	ghc-vector-algorithms-prof >= 0.6
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base >= 4.10
Requires:	ghc-bytestring >= 0.9
Requires:	ghc-containers >= 0.5.8
Requires:	ghc-hashable
Requires:	ghc-split >= 0.2
Requires:	ghc-text >= 0.11
Requires:	ghc-transformers >= 0.3
Requires:	ghc-unordered-containers >= 0.2
Requires:	ghc-vector >= 0.10
Requires:	ghc-vector-algorithms >= 0.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Type classes for mapping, folding, and traversing monomorphic and
polymorphic containers. Haskell is good at operating over polymorphic
containers such as a list [a]. A monomorphic container is one such as
Text which has a type Text that does not expose a type variable for
the underlying characters.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
BuildRequires:	ghc-base-prof >= 4.10
BuildRequires:	ghc-bytestring-prof >= 0.9
BuildRequires:	ghc-containers-prof >= 0.5.8
BuildRequires:	ghc-hashable-prof
BuildRequires:	ghc-split-prof >= 0.2
BuildRequires:	ghc-text-prof >= 0.11
BuildRequires:	ghc-transformers-prof >= 0.3
BuildRequires:	ghc-unordered-containers-prof >= 0.2
BuildRequires:	ghc-vector-prof >= 0.10
BuildRequires:	ghc-vector-algorithms-prof >= 0.6

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc ChangeLog.md LICENSE README.md %{name}-%{version}-doc/html
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/MonoTraversable
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/MonoTraversable/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/MonoTraversable/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/MonoTraversable/*.p_hi
%endif
