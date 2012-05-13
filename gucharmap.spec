%define api	2_90
%define major 7
%define gir_major	2.90
%define libname		%mklibname %{name} %{api} %{major}
%define develname	%mklibname -d %{name}
%define girname		%mklibname %{name}-gir %{gir_major}

Summary: 	A Unicode character map and font viewer
Name: 		gucharmap
Version:	3.4.1.1
Release: 	1
License: 	GPLv2+
Group: 		Publishing
Source0: 	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz
URL: 		http://gucharmap.sourceforge.net/
BuildRequires:	gnome-doc-utils >= 0.3.2
BuildRequires:	intltool
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)

%description
gucharmap is a Unicode/ISO 10646 character map and font viewer. It
supports anti-aliased, scalable truetype fonts in X, using Xft, and
works on Unix and Windows platforms.

%package -n %{libname}
Summary: Main library for gucharmap
Group: System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with gucharmap.

%package -n %{girname}
Summary: GObject Introspection interface description for %{name}
Group: System/Libraries
Requires: %{libname} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{develname}
Summary: Headers for developing programs that will use gucharmap
Group: Development/GNOME and GTK+
Requires: %{libname} = %{version}
Provides: %{name}-devel = %{version}-%{release}

%description -n %{develname}
This package contains the headers that programmers will need to develop
applications which will use gucharmap.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static \
	--with-gtk=3.0 \
	--enable-introspection \
	--disable-scrollkeeper 

%make LIBS='-lgmodule-2.0'

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang %{name} --with-gnome

%files -f %{name}.lang
%doc README TODO
%{_bindir}/*
%{_datadir}/glib-2.0/schemas/
%{_datadir}/applications/*

%files -n %{libname}
%{_libdir}/libgucharmap_%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Gucharmap-%{gir_major}.typelib

%files -n %{develname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/gir-1.0/Gucharmap-%{gir_major}.gir

