#
# Conditional build:
%bcond_without	glade		# Glade catalog

Summary:	GTK+ git repository viewer
Summary(pl.UTF-8):	Przeglądarka repozytoriów git oparta na GTK+
Name:		gitg
Version:	3.32.1
Release:	4
License:	GPL v2
Group:		Development/Tools
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gitg/3.32/%{name}-%{version}.tar.xz
# Source0-md5:	da45a04be28d23638d020a7155d28343
URL:		https://wiki.gnome.org/Apps/Gitg
BuildRequires:	gettext-tools >= 0.17
%{?with_glade:BuildRequires:	glade-devel >= 3.2}
BuildRequires:	glib2-devel >= 1:2.38
BuildRequires:	gobject-introspection-devel >= 0.10.1
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+3-devel >= 3.20.0
BuildRequires:	gtksourceview3-devel >= 3.10
BuildRequires:	gtkspell3-devel >= 3.0.3
BuildRequires:	libdazzle-devel
BuildRequires:	libgee-devel >= 0.8
# libgit2 with threading support
BuildRequires:	libgit2-devel >= 0.20.0-3
BuildRequires:	libgit2-glib-devel >= 0.27.8
BuildRequires:	libpeas-devel >= 1.5.0
BuildRequires:	libsecret-devel
BuildRequires:	libsoup-devel >= 2.4
BuildRequires:	libxml2-devel >= 1:2.9.0
BuildRequires:	meson >= 0.48.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3.2.3
BuildRequires:	python3-pygobject3-devel >= 3.0.0
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.32.0
BuildRequires:	vala-gtkspell3
BuildRequires:	vala-libdazzle
BuildRequires:	vala-libgee >= 0.8
BuildRequires:	vala-libgit2-glib >= 0.27.8
BuildRequires:	vala-libsecret
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Requires(post,preun):	glib2 >= 1:2.38
Requires(post,postun):	gtk-update-icon-cache
Requires:	glib2 >= 1:2.38
Requires:	gtk+3 >= 3.20.0
Requires:	gtksourceview3 >= 3.10
Requires:	gtkspell3 >= 3.0.3
Requires:	libgit2 >= 0.20.0-3
Requires:	libgit2-glib >= 0.27.8
Requires:	libxml2 >= 1:2.9.0
Obsoletes:	gitg-static < 3.30.1
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
Requires:	gtk+3-devel >= 3.20.0
Requires:	libgee-devel >= 0.8
Requires:	libgit2-devel >= 0.20.0-3
Requires:	libgit2-glib-devel >= 0.27.8

%description devel
libgitg header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libgitg.

%package glade
Summary:	libgitg catalog file for Glade
Summary(pl.UTF-8):	Plik katalogu libgitg dla Glade
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	glade >= 3.2

%description glade
libgitg catalog file for Glade.

%description glade -l pl.UTF-8
Plik katalogu libgitg dla Glade.

%package -n python3-gitg
Summary:	Python 3.x binding to GitgExt library
Summary(pl.UTF-8):	Wiązanie Pythona 3.x do biblioteki GitgExt
Group:		Libraries/Python
Requires:	python3-libs >= 1:3.2.3
Requires:	python3-pygobject3 >= 3.0.0
Requires:	%{name} = %{version}-%{release}

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
Requires:	vala >= 2:0.32
BuildArch:	noarch

%description -n vala-gitg
Vala API for Gitg libraries.

%description -n vala-gitg -l pl.UTF-8
API języka Vala do bibliotek Gitg.

%prep
%setup -q

%build
%meson build \
	-Dglade_catalog=%{__true_false glade} \
	-Dpython=true
# -Ddocs=true is nop (as of 3.32.1)

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

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
%doc AUTHORS ChangeLog NEWS README.md
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
%{_datadir}/metainfo/org.gnome.gitg.appdata.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gitg.gschema.xml
%{_desktopdir}/org.gnome.gitg.desktop
%{_mandir}/man1/gitg.1*
%{_iconsdir}/hicolor/*x*/apps/org.gnome.gitg.png
%{_iconsdir}/hicolor/scalable/apps/org.gnome.gitg-symbolic.svg

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgitg-1.0.so
%attr(755,root,root) %{_libdir}/libgitg-ext-1.0.so
%dir %{_includedir}/libgitg-1.0
%dir %{_includedir}/libgitg-1.0/libgitg
%{_includedir}/libgitg-1.0/libgitg/libgitg.h
%dir %{_includedir}/libgitg-ext-1.0
%dir %{_includedir}/libgitg-ext-1.0/libgitg-ext
%{_includedir}/libgitg-ext-1.0/libgitg-ext/libgitg-ext.h
%{_datadir}/gir-1.0/Gitg-1.0.gir
%{_datadir}/gir-1.0/GitgExt-1.0.gir
%{_pkgconfigdir}/libgitg-1.0.pc
%{_pkgconfigdir}/libgitg-ext-1.0.pc

%if %{with glade}
%files glade
%defattr(644,root,root,755)
%{_datadir}/glade/catalogs/gitg-glade.xml
%endif

%files -n python3-gitg
%defattr(644,root,root,755)
%{py3_sitedir}/gi/overrides/GitgExt.py

%files -n vala-gitg
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libgitg-1.0.vapi
%{_datadir}/vala/vapi/libgitg-ext-1.0.vapi
