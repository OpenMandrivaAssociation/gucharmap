%define major 7
%define libname %mklibname %name %major
%define develname %mklibname -d %name

Summary: 	A Unicode character map and font viewer
Name: 		gucharmap
Version:	3.0.1
Release: 	%mkrel 4
License: 	GPLv2+
Group: 		Publishing
Source0: 	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Source1: 	%{name}48.png
Source2: 	%{name}32.png
Source3: 	%{name}16.png
URL: 		http://gucharmap.sourceforge.net/
BuildRequires: 	gtk+2-devel
BuildRequires:	libGConf2-devel
BuildRequires:	scrollkeeper
BuildRequires:	gnome-doc-utils >= 0.3.2
BuildRequires:	libxslt-proc
BuildRequires:	intltool

%description
gucharmap is a Unicode/ISO 10646 character map and font viewer. It
supports anti-aliased, scalable truetype fonts in X, using Xft, and
works on Unix and Windows platforms.

%package -n %libname
Summary: Main library for gucharmap
Group: System/Libraries

%description -n %libname
This package contains the library needed to run programs dynamically
linked with gucharmap.

%package -n %develname
Summary: Headers for developing programs that will use gucharmap
Group: Development/GNOME and GTK+
Requires: %libname = %{version}
Provides: lib%name-devel = %{version}-%{release}
Provides: %name-devel = %{version}-%{release}
Requires: libgnomeui2-devel
Obsoletes: %mklibname -d %name 6

%description -n %develname
This package contains the headers that programmers will need to develop
applications which will use gucharmap.

%prep
%setup -q

%build
%configure2_5x --enable-gnome --disable-scrollkeeper --with-gtk=2.0
%make

%install
rm -rf %{buildroot} %name.lang

%makeinstall_std

#icons
mkdir -p %{buildroot}/%_liconsdir
cat %SOURCE1 > %{buildroot}/%_liconsdir/%name.png
mkdir -p %{buildroot}/%_iconsdir
cat %SOURCE2 > %{buildroot}/%_iconsdir/%name.png
mkdir -p %{buildroot}/%_miconsdir
cat %SOURCE3 > %{buildroot}/%_miconsdir/%name.png

%{find_lang} %{name} --with-gnome

%preun
%preun_uninstall_gconf_schemas %name
 
%files -f %{name}.lang
%defattr (-,root,root)
%doc README TODO
%_sysconfdir/gconf/schemas/%name.schemas
%{_bindir}/*
%{_datadir}/applications/*
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png

%files -n %libname
%defattr (-,root,root)
%_libdir/libgucharmap.so.%{major}*

%files -n %develname
%defattr (-,root,root)
%_libdir/*.so
%_libdir/pkgconfig/*
%_includedir/*
