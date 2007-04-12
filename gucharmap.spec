%define major 6
%define libname %mklibname %name %major

Summary: 	A Unicode character map and font viewer
Name: 		gucharmap
Version: 1.10.0
Release: 	%mkrel 1
License: 	GPL
Group: 		Publishing
Source0: 	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Source1: 	%{name}48.png
Source2: 	%{name}32.png
Source3: 	%{name}16.png

URL: 		http://gucharmap.sourceforge.net/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: 	libgnomeui2-devel >= 2.5.90.1
BuildRequires:	scrollkeeper
BuildRequires:	gnome-doc-utils >= 0.3.2
BuildRequires:	libxslt-proc
BuildRequires:	perl-XML-Parser
BuildRequires:	desktop-file-utils
Requires(post):		scrollkeeper
Requires(postun):		scrollkeeper

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

%package -n %libname-devel
Summary: Headers for developing programs that will use gucharmap
Group: Development/GNOME and GTK+
Requires: %libname = %{version}
Provides: lib%name-devel = %{version}-%{release}
Provides: %name-devel = %{version}-%{release}
Requires: libgnomeui2-devel

%description -n %libname-devel
This package contains the headers that programmers will need to develop
applications which will use gucharmap.

%prep
%setup -q
touch *

%build

%configure2_5x --enable-gnome --disable-scrollkeeper
%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang

%makeinstall_std

mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}):\
command="%{_bindir}/gucharmap" \
title="Unicode Character Map" \
longtitle="Unicode Character Map" \
needs="x11" \
icon="gucharmap.png" \
section="Office/Accessories" xdg="true"
EOF
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Office-Accessories" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
cat %SOURCE1 > $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
cat %SOURCE2 > $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
cat %SOURCE3 > $RPM_BUILD_ROOT/%_miconsdir/%name.png

%{find_lang} %{name} --with-gnome
for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done

%post
%update_scrollkeeper
%update_menus
 
%postun
%clean_scrollkeeper
%clean_menus

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr (-,root,root)
%doc ChangeLog README TODO
%{_bindir}/*
%{_menudir}/*
%{_datadir}/applications/*
%_datadir/icons/hicolor/48x48/apps/%name.png
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png
%dir %{_datadir}/omf/%{name}
%{_datadir}/omf/gucharmap/gucharmap-C.omf

%files -n %libname
%defattr (-,root,root)
%_libdir/libgucharmap.so.%{major}*

%files -n %libname-devel
%defattr (-,root,root)
%_libdir/*.so
%attr(644,root,root) %_libdir/*.la
%_libdir/pkgconfig/*
%_includedir/*


