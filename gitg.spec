Summary:	GTK+ git repository viewer
Summary(pl.UTF-8):	Przeglądarka repozytoriów git oparta na GTK+
Name:		gitg
Version:	0.2.7
Release:	0.1
License:	GPL v2
Group:		Development/Tools
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gitg/0.2/%{name}-%{version}.tar.xz
# Source0-md5:	54010e00f2fc6d21f121b51259f8abfe
URL:		http://trac.novowork.com/gitg/
BuildRequires:	GConf2-devel >= 2.24.0
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gsettings-desktop-schemas-devel
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtksourceview3-devel >= 3.1.3
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Requires(post,preun):	glib2 >= 1:2.26.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	glib2 >= 1:2.26.0
Requires:	gtksourceview3 >= 3.1.3
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
Requires:	glib2-devel >= 1:2.26.0

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
Biblioteka statyczna libgitg

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
%doc AUTHORS ChangeLog MAINTAINERS NEWS README
%attr(755,root,root) %{_bindir}/gitg
%attr(755,root,root) %{_libdir}/libgitg-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgitg-1.0.so.0
%{_datadir}/gitg
%{_datadir}/glib-2.0/schemas/org.gnome.gitg.gschema.xml
%{_desktopdir}/gitg.desktop
%{_mandir}/man1/gitg.1*
%{_iconsdir}/hicolor/*/apps/gitg.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgitg-1.0.so
%{_includedir}/libgitg-1.0
%{_pkgconfigdir}/libgitg-1.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgitg-1.0.a
