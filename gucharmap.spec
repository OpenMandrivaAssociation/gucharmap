%define url_ver %(echo %{version}|cut -d. -f1,2)

%define api	2_90
%define major	7
%define gimajor	2.90
%define libname	%mklibname %{name} %{api} %{major}
%define girname	%mklibname %{name}-gir %{gimajor}
%define devname	%mklibname -d %{name}

%define _disable_rebuild_configure 1

Summary:	A Unicode character map and font viewer
Name:		gucharmap
Version:	13.0.4
Release:	1
License:	GPLv2+
Group:		Publishing
Url:		http://gucharmap.sourceforge.net/
Source0:	https://gitlab.gnome.org/GNOME/gucharmap/-/archive/%{version}/%{name}-%{version}.tar.bz2
#Source0:	http://ftp.gnome.org/pub/GNOME/sources/gucharmap/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires: meson
BuildRequires: intltool
BuildRequires: itstool
BuildRequires: xsltproc
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gnome-doc-utils)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(vapigen)
BuildRequires: gtk-doc
BuildRequires: scrollkeeper
BuildRequires: unicode-ucd
BuildRequires: perl(Env)

%description
gucharmap is a Unicode/ISO 10646 character map and font viewer. It
supports anti-aliased, scalable truetype fonts in X, using Xft, and
works on Unix and Windows platforms.

%package -n %{libname}
Summary:	Main library for gucharmap
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with gucharmap.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{devname}
Summary:	Headers for developing programs that will use gucharmap
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the headers that programmers will need to develop
applications which will use gucharmap.

%prep
%setup -q

%build
%meson -D ucd_path=%{_datadir}/unicode/ucd
#       -D vapi=false 

%meson_build

%install
%meson_install
%find_lang %{name} --with-gnome

%files -f %{name}.lang
%doc README TODO
%{_bindir}/*
%{_datadir}/glib-2.0/schemas/
%{_datadir}/applications/*
%{_datadir}/appdata/gucharmap.appdata.xml

%files -n %{libname}
%{_libdir}/libgucharmap_%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Gucharmap-%{gimajor}.typelib

%files -n %{devname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/gir-1.0/Gucharmap-%{gimajor}.gir
