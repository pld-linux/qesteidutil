#
# Conditional build:
%bcond_with	qt5		# Use Qt5 (instead of Qt4)

%define		qt4ver	4.8.0
Summary:	Estonian ID card utility
Name:		qesteidutil
# NOTE: update to 3.12.10 is on dev-3.12 branch, but fails to compile
Version:	3.8.0.1106
Release:	1
License:	LGPL v2+
Group:		X11/Applications
Source0:	https://installer.id.ee/media/sources/%{name}-%{version}.tar.gz
# Source0-md5:	4e5a792fa4de027d367a26b4f0b82ac1
Patch0:		system_qtsingleapplication.patch
Patch1:		desktop.patch
URL:		http://www.ria.ee/
BuildRequires:	cmake >= 2.8
BuildRequires:	desktop-file-utils
BuildRequires:	openssl-devel
BuildRequires:	pcsc-lite-devel
%if %{with qt5}
BuildRequires:	Qt5Network-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	qt5-build
BuildRequires:	qt5-linguist
BuildRequires:	qt5-qmake
%else
BuildRequires:	QtGui-devel >= %{qt4ver}
BuildRequires:	QtNetwork-devel >= %{qt4ver}
BuildRequires:	QtSingleApplication-devel >= 2.6.1
BuildRequires:	qt4-build
BuildRequires:	qt4-linguist
BuildConflicts:	Qt5Widgets-devel
%endif
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
QEsteidUtil is an application for managing Estonian ID Card. In an
user-friendly interface it is possible to change and unlock PINs,
examine detailed information about personal data file on the card,
extract and view certificates, set up mobile ID, and configure
@eesti.ee email.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# Remove bundled qtsingleapplication to make sure it isn't used
rm -r qtsingleapplication

%build
install -d build
cd build
%cmake \
%ifarch %{arm} %{ix86} %{x8664}
	-DBREAKPAD=ON \
%endif
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/qesteidutil.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc AUTHORS README RELEASE-NOTES.txt
%attr(755,root,root) %{_bindir}/qesteidutil
%{_mandir}/man1/qesteidutil.1*
%{_desktopdir}/qesteidutil.desktop
%{_iconsdir}/hicolor/*/apps/qesteidutil.png
