Summary:	Gtk+ git repository viewer
Name:		gitg
Version:	0.2.0
Release:	0.1
License:	GPL v2
Group:		Development/Tools
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gitg/0.2/%{name}-%{version}.tar.bz2
# Source0-md5:	6d2b78d7686a84b52d7316c5eedf3ba1
URL:		http://trac.novowork.com/gitg/
BuildRequires:	GConf2-devel >= 2.24.0
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.8
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtksourceview3-devel >= 2.90.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,preun):	GConf2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gitg is a git repository viewer targeting gtk+/GNOME. One of its main
objectives is to provide a more unified user experience for git
frontends across multiple desktops.

%package devel
Summary:	libgitg header files
Summary(pl.UTF-8):	Pliki nagłówkowe libgitg
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
libgitg header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe libgitg.

%package static
Summary:	libgitg static libraries
Summary(pl.UTF-8):	Biblioteki statyczne libgitg
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
libgitg static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne libgitg

%prep
%setup -q

%build
%{__libtoolize}
%{__intltoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgitg-1.0.la

%find_lang gitg

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%glib_compile_schemas
%update_icon_cache hicolor

%postun
if [ "$1" = "0" ]; then
	/sbin/ldconfig
	%glib_compile_schemas
	%update_icon_cache hicolor
fi

%files -f gitg.lang
%defattr(644,root,root,755)
%doc README ChangeLog AUTHORS NEWS
%attr(755,root,root) %{_bindir}/gitg
%attr(755,root,root) %ghost %{_libdir}/libgitg-1.0.so.0
%attr(755,root,root) %{_libdir}/libgitg-1.0.so.*.*.*
%{_datadir}/gitg
%{_datadir}/glib-2.0/schemas/org.gnome.gitg.gschema.xml
%{_desktopdir}/gitg.desktop
%{_mandir}/man1/gitg.1*
%{_iconsdir}/hicolor/*/apps/gitg.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libgitg-1.0.so
%{_includedir}/libgitg-1.0
%{_pkgconfigdir}/libgitg-1.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgitg-1.0.a
