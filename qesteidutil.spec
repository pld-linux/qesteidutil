Summary:	Estonian ID card utility
Name:		qesteidutil
Version:	0.3.0
Release:	1
License:	LGPL v2+
Group:		X11/Applications
URL:		http://code.google.com/p/esteid/
Source0:	http://esteid.googlecode.com/files/%{name}-%{version}.tar.bz2
# Source0-md5:	f91ddc6022ecf86753dc3492a8e33baf
# Use system qtsingleapplication, backported from upstream SVN
Patch0:		%{name}-0.3.0-system_qtsingleapplication.patch
Patch1:		desktop.patch
BuildRequires:	QtSingleApplication-devel
BuildRequires:	QtWebKit-devel
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	libp11-devel
BuildRequires:	openssl-devel
BuildRequires:	qt4-build
BuildRequires:	smartcardpp-devel
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
%patch0 -p0
%patch1 -p1

# Remove bundled qtsingleapplication to make sure it isn't used
rm -rf qtsingleapplication

%build
install -d build
cd build
%cmake ..
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
%doc AUTHORS NEWS README
%attr(755,root,root) %{_bindir}/qesteidutil
%{_desktopdir}/qesteidutil.desktop
%{_iconsdir}/hicolor/*/apps/qesteidutil.png
