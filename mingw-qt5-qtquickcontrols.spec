%?mingw_package_header

%global qt_module qtquickcontrols
#%%global pre rc1

#%%global snapshot_date 20121112
#%%global snapshot_rev a73dfa7c

%if 0%{?snapshot_date}
%global source_folder qt-%{qt_module}
%else
%global source_folder %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}
%endif

# first two digits of version
%global release_version %(v=%{version}; echo ${v%.${v#[0-9].[0-9].}})

Name:           mingw-qt5-%{qt_module}
Version:        5.6.0
Release:        3%{?pre:.%{pre}}%{?snapshot_date:.git%{snapshot_date}.%{snapshot_rev}}%{?dist}
Summary:        Qt5 for Windows - QtQuickControls component

License:        GPLv3 with exceptions or LGPLv2 with exceptions
Group:          Development/Libraries
URL:            http://qt-project.org/

%if 0%{?snapshot_date}
# To regenerate:
# wget http://qt.gitorious.org/qt/%{qt_module}/archive-tarball/%{snapshot_rev} -O qt5-%{qt_module}-%{snapshot_rev}.tar.gz
Source0:        qt5-%{qt_module}-%{snapshot_rev}.tar.gz
%else
%if "%{?pre}" != ""
Source0:        http://download.qt-project.org/development_releases/qt/%{release_version}/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0:        http://download.qt-project.org/official_releases/qt/%{release_version}/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif
%endif

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 96
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-qt5-qtbase >= 5.5.1
BuildRequires:  mingw32-qt5-qtdeclarative >= 5.5.1

BuildRequires:  mingw64-filesystem >= 96
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-qt5-qtbase >= 5.5.1
BuildRequires:  mingw64-qt5-qtdeclarative >= 5.5.1


%description
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win32
%package -n mingw32-qt5-%{qt_module}
Summary:        Qt5 for Windows - QtQuickControls component

%description -n mingw32-qt5-%{qt_module}
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win64
%package -n mingw64-qt5-%{qt_module}
Summary:        Qt5 for Windows - QtQuickControls component

%description -n mingw64-qt5-%{qt_module}
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


%?mingw_debug_package


%prep
%setup -q -n %{source_folder}


%build
%mingw_qmake_qt5 ../%{qt_module}.pro
%mingw_make %{?_smp_mflags}


%install
%mingw_make install INSTALL_ROOT=%{buildroot}

# Create a list of .dll.debug files which need to be excluded from the main packages
# We do this to keep the %%files section as clean/readable as possible (otherwise every
# single file and directory would have to be mentioned individually in the %%files section)
# Note: the .dll.debug files aren't created yet at this point (as it happens after
# the %%install section). Therefore we have to assume that all .dll files will
# eventually get a .dll.debug counterpart
find %{buildroot}%{mingw32_prefix} | grep .dll | grep -v .dll.a | sed s@"^%{buildroot}"@"%%exclude "@ | sed s/".dll\$"/".dll.debug"/ > mingw32-qt5-%{qt_module}.excludes
find %{buildroot}%{mingw64_prefix} | grep .dll | grep -v .dll.a | sed s@"^%{buildroot}"@"%%exclude "@ | sed s/".dll\$"/".dll.debug"/ > mingw64-qt5-%{qt_module}.excludes


# Win32
%files -n mingw32-qt5-%{qt_module} -f mingw32-qt5-%{qt_module}.excludes
%{mingw32_datadir}/qt5/qml/QtQuick/Controls/
%{mingw32_datadir}/qt5/qml/QtQuick/Dialogs/
%{mingw32_datadir}/qt5/qml/QtQuick/Extras/
%{mingw32_datadir}/qt5/qml/QtQuick/Layouts/
%{mingw32_datadir}/qt5/qml/QtQuick/PrivateWidgets/

# Win64
%files -n mingw64-qt5-%{qt_module} -f mingw64-qt5-%{qt_module}.excludes
%{mingw64_datadir}/qt5/qml/QtQuick/Controls/
%{mingw64_datadir}/qt5/qml/QtQuick/Dialogs/
%{mingw64_datadir}/qt5/qml/QtQuick/Extras/
%{mingw64_datadir}/qt5/qml/QtQuick/Layouts/
%{mingw64_datadir}/qt5/qml/QtQuick/PrivateWidgets/


%changelog
* Fri Feb 03 2017 Jajauma's Packages <jajauma@yandex.ru> - 5.6.0-3
- Rebuild with GCC 5.4.0

* Thu Sep 01 2016 Martin Bříza <mbriza@redhat.com> - 5.6.0-2
- Specfile tweaks

* Fri Jul 29 2016 Przemysław Palacz <pprzemal@gmail.com> - 5.6.0-1
- Update to 5.6.0

* Wed Mar 23 2016 Przemysław Palacz <pprzemal@gmail.com> - 5.5.1-2
- Rebuilt against latest mingw-qt5-qtbase

* Mon Mar 07 2016 Przemysław Palacz <pprzemal@gmail.com> - 5.5.1-1
- Update to 5.5.1

* Tue Mar 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.1-1
- Update to 5.4.1

* Thu Jan  1 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.0-1
- Update to 5.4.0

* Sun May 25 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.0-1
- Update to 5.3.0
- Make sure the .dll.a files are included in the main packages

* Sat Feb  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.1-1
- Update to 5.2.1

* Sun Jan 12 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-2
- Don't carry .dll.debug files in main package

* Sun Jan  5 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-1
- Update to 5.2.0

* Fri Nov 29 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-0.1.rc1
- Initial release

