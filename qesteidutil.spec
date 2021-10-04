#
# Conditional build:
%bcond_with	breakpad		# build without breakpad crash reporting

%ifnarch %{arm} %{ix86} %{x8664}
%undefine	with_breakpad
%endif

Summary:	Estonian ID card utility
Name:		qesteidutil
Version:	3.12.10
Release:	3
License:	LGPL v2+
Group:		X11/Applications
Source0:	https://github.com/open-eid/qesteidutil/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4e3805d3449e94427a67f5dfe7bae3c9
Patch0:		system_qtsingleapplication.patch
Patch1:		desktop.patch
Patch2:		qt-5.11.patch
URL:		https://github.com/open-eid/qesteidutil
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Network-devel
BuildRequires:	Qt5SingleApplication-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	appstream-glib
BuildRequires:	cmake >= 3.0
BuildRequires:	desktop-file-utils
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel
BuildRequires:	pcsc-lite-devel
BuildRequires:	qt5-build
BuildRequires:	qt5-linguist
BuildRequires:	qt5-qmake
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
%patch2 -p1

# Remove bundled qtsingleapplication to make sure it isn't used
rm -r common/qtsingleapplication

%build
install -d build
cd build
%cmake \
%if %{without breakpad}
	-DBREAKPAD="" \
%endif
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/qesteidutil.desktop
appstream-util validate-relax --nonet $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md RELEASE-NOTES.md
%attr(755,root,root) %{_bindir}/qesteidutil
%{_mandir}/man1/qesteidutil.1*
%{_datadir}/appdata/qesteidutil.appdata.xml
%{_desktopdir}/qesteidutil.desktop
%{_iconsdir}/hicolor/*/apps/qesteidutil.png
