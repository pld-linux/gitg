# TODO: glade catalog?
#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	GTK+ git repository viewer
Summary(pl.UTF-8):	Przeglądarka repozytoriów git oparta na GTK+
Name:		gitg
Version:	3.14.0
Release:	0.1
License:	GPL v2
Group:		Development/Tools
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gitg/3.14/%{name}-%{version}.tar.xz
# Source0-md5:	6cfd9cf5b219379b7144f1197b1cbc7a
URL:		http://live.gnome.org/Gitg
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	glib2-devel >= 1:2.38
BuildRequires:	gobject-introspection-devel >= 0.10.1
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+3-devel >= 3.10.0
BuildRequires:	gtk-webkit3-devel >= 2.2
BuildRequires:	gtksourceview3-devel >= 3.10
BuildRequires:	gtkspell3-devel >= 3.0.3
BuildRequires:	intltool >= 0.40.0
BuildRequires:	json-glib-devel
BuildRequires:	libgee-devel >= 0.8
# libgit2 with threading support
BuildRequires:	libgit2-devel >= 0.20.0-3
BuildRequires:	libgit2-glib-devel >= 0.0.10
BuildRequires:	libpeas-devel >= 1.5.0
BuildRequires:	libpeas-gtk-devel >= 1.5.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 3.2.3
BuildRequires:	python3-pygobject3-devel >= 3.0.0
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.20.1.23
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Requires(post,preun):	glib2 >= 1:2.38
Requires(post,postun):	gtk-update-icon-cache
Requires:	glib2 >= 1:2.38
Requires:	gtk+3 >= 3.10.0
Requires:	gtk-webkit3 >= 2.2
Requires:	gtksourceview3 >= 3.10
Requires:	gtkspell3 >= 3.0.3
Requires:	libgit2 >= 0.20.0-3
Requires:	libgit2-glib >= 0.0.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gitg is a git repository viewer targeting GTK+/GNOME. One of its main
objectives is to provide a more unified user experience for git
frontends across multiple desktops.

%description -l pl.UTF-8
gitg to przeglądarka repozytoriów git przeznaczona dla środowisk
GTK+/GNOME. Jednym z głównych celów jest zapewnienie bardziej
ujednoliconego sposobu obsługi dla frontendów gita w wielu
środowiskach graficznych.

%package devel
Summary:	libgitg header files
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libgitg
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.38
Requires:	gtk+3-devel >= 3.10.0
Requires:	libgit2-devel >= 0.20.0-3
Requires:	libgit2-glib-devel >= 0.0.10

%description devel
libgitg header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libgitg.

%package static
Summary:	libgitg static library
Summary(pl.UTF-8):	Biblioteka statyczna libgitg
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
libgitg static library.

%description static -l pl.UTF-8
Biblioteka statyczna libgitg.

%package -n python3-gitg
Summary:	Python 3.x binding to GitgExt library
Summary(pl.UTF-8):	Wiązanie Pythona 3.x do biblioteki GitgExt
Group:		Python/Libraries
Requires:	%{name} = %{version}-%{release}
BuildRequires:	python3-libs >= 3.2.3
BuildRequires:	python3-pygobject3 >= 3.0.0

%description -n python3-gitg
Python 3.x binding to GitgExt library, allowing to write Gitg plugins
in Python.

%description -n python3-gitg -l pl.UTF-8
Wiązanie Pythona 3.x do biblioteki GitgExt, pozwalające na tworzenie
wtyczek Gitg w Pythonie.

%package -n vala-gitg
Summary:	Vala API for Gitg libraries
Summary(pl.UTF-8):	API języka Vala do bibliotek Gitg
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.20.1.23

%description -n vala-gitg
Vala API for Gitg libraries.

%description -n vala-gitg -l pl.UTF-8
API języka Vala do bibliotek Gitg.

%prep
%setup -q

%build
%{__libtoolize}
%{__intltoolize}
%{__aclocal} -I m4 -I libgd
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgitg-*.la \
	$RPM_BUILD_ROOT%{_libdir}/gitg/plugins/*.la
%if %{with static_libs}
%{__rm}	$RPM_BUILD_ROOT%{_libdir}/gitg/plugins/*.a
%endif

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
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gitg
%attr(755,root,root) %{_libdir}/libgitg-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgitg-1.0.so.0
%attr(755,root,root) %{_libdir}/libgitg-ext-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgitg-ext-1.0.so.0
%{_libdir}/girepository-1.0/Gitg-1.0.typelib
%{_libdir}/girepository-1.0/GitgExt-1.0.typelib
%dir %{_libdir}/gitg
%dir %{_libdir}/gitg/plugins
%attr(755,root,root) %{_libdir}/gitg/plugins/libdiff.so
%{_libdir}/gitg/plugins/diff.plugin
%attr(755,root,root) %{_libdir}/gitg/plugins/libfiles.so
%{_libdir}/gitg/plugins/files.plugin
%{_datadir}/gitg
%{_datadir}/appdata/gitg.appdata.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gitg.gschema.xml
%{_desktopdir}/gitg.desktop
%{_mandir}/man1/gitg.1*
%{_iconsdir}/hicolor/*/apps/gitg.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgitg-1.0.so
%attr(755,root,root) %{_libdir}/libgitg-ext-1.0.so
%{_includedir}/libgitg-1.0
%{_includedir}/libgitg-ext-1.0
%{_datadir}/gir-1.0/Gitg-1.0.gir
%{_datadir}/gir-1.0/GitgExt-1.0.gir
%{_pkgconfigdir}/libgitg-1.0.pc
%{_pkgconfigdir}/libgitg-ext-1.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgitg-1.0.a
%{_libdir}/libgitg-ext-1.0.a
%endif

%files -n python3-gitg
%defattr(644,root,root,755)
%{py3_sitedir}/gi/overrides/GitgExt.py
%{py3_sitedir}/gi/overrides/__pycache__/GitgExt.cpython-*.py[co]

%files -n vala-gitg
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libgitg-1.0.vapi
%{_datadir}/vala/vapi/libgitg-ext-1.0.vapi
