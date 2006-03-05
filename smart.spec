# TODO
# - bundled and modified software:
#  - pexpect-0.999 http://pexpect.sourceforge.net/
# - sudo or sth for 'usermode' replacement for 'smart-root'
%define	module smart
Summary:	Next generation package handling tool
Name:		smart
Version:	0.41
Release:	0.26.11
License:	GPL
Group:		Applications/System
URL:		http://labix.org/smart/
Source0:	http://labix.org/download/smart/%{name}-%{version}.tar.bz2
# Source0-md5:	1460dfbfe7f739ac718525c71f46b5fc
Source1:	%{name}.console
Source2:	%{name}.pam
Source3:	%{name}.desktop
Source4:	%{name}-distro.py
Patch0:		%{name}-mxddcl.patch
Patch1:		%{name}-syslibs.patch
Patch2:		%{name}-optflags.patch
BuildRequires:	kdelibs-devel
BuildRequires:	libstdc++-devel
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	sed >= 4.0
Requires:	python-cElementTree
Requires:	python-elementtree
Requires:	python-rpm
%pyrequires_eq  python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Smart Package Manager is a next generation package handling tool.

%package update
Summary:	Allows execution of 'smart update' by normal users (suid)
Group:		Applications/System
Requires:	smart = %{version}-%{release}

%description update
Allows execution of 'smart update' by normal users through a special
suid command.

%package gui
Summary:	Graphical user interface for the smart package manager
Group:		Applications/System
Requires:	python-pygtk-gtk
Requires:	smart = %{version}-%{release}

%description gui
Graphical user interface for the smart package manager.

%package -n ksmarttray
Summary:	KDE tray program for watching updates with Smart Package Manager
Group:		Applications/System
Requires:	smart-update = %{version}-%{release}

%description -n ksmarttray
KDE tray program for watching updates with Smart Package Manager.

%description -n ksmarttray
Programa tray do KDE para verificar atualizações com o Smart Package Manager.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
# %{_libdir} is hardcoded
%{__sed} -i -e's,/usr/lib/,%{_libdir}/,' smart/const.py

rm -rf smart/util/elementtree
rm -rf smart/util/celementtree
rm -f smart/util/optparse.py

%build
export CFLAGS="%{rpmcflags}"
python setup.py build

# smart-update
%{__make} -C contrib/smart-update \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

# ksmarttray
cd contrib/ksmarttray
%{__make} -f admin/Makefile.common
%configure \
%if "%{_lib}" == "lib64"
    --enable-libsuffix=64 \
%endif
    --%{?debug:en}%{!?debug:dis}able-debug%{?debug:=full} \
    --with-qt-libraries=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{pam.d,security/console.apps},%{_desktopdir},%{_pixmapsdir},%{_libdir}/smart,/var/lib/smart}
python setup.py install -O1 --root=$RPM_BUILD_ROOT

ln -sf smart $RPM_BUILD_ROOT%{_bindir}/smart-root
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/security/console.apps/smart-root
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/smart-root
cp -f contrib/smart-update/smart-update $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}
install -p smart/interfaces/images/smart.png $RPM_BUILD_ROOT%{_pixmapsdir}/smart.png
# Currently needs to hardcode %{_libdir}, as this is hardcoded in the
# code, too.
install -p %{SOURCE4} $RPM_BUILD_ROOT%{_libdir}/smart/distro.py

%{__make} install \
	-C contrib/ksmarttray \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc HACKING README LICENSE TODO IDEAS
%attr(755,root,root) %{_bindir}/smart
%attr(755,root,root) %{_bindir}/smart-root
%config /etc/security/console.apps/smart-root
%config /etc/pam.d/smart-root
%{_libdir}/smart
%dir /var/lib/smart

%attr(755,root,root) %{py_sitedir}/%{module}/ccache.so
%attr(755,root,root) %{py_sitedir}/%{module}/util/cdistance.so
%attr(755,root,root) %{py_sitedir}/%{module}/util/ctagfile.so
%attr(755,root,root) %{py_sitedir}/%{module}/backends/deb/cdebver.so
%attr(755,root,root) %{py_sitedir}/%{module}/backends/rpm/crpmver.so

%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%dir %{py_sitedir}/%{module}/backends
%{py_sitedir}/%{module}/backends/*.py[co]
%dir %{py_sitedir}/%{module}/backends/deb
%{py_sitedir}/%{module}/backends/deb/*.py[co]
%dir %{py_sitedir}/%{module}/backends/rpm
%{py_sitedir}/%{module}/backends/rpm/*.py[co]
%dir %{py_sitedir}/%{module}/backends/slack
%{py_sitedir}/%{module}/backends/slack/*.py[co]
%dir %{py_sitedir}/%{module}/channels
%{py_sitedir}/%{module}/channels/*.py[co]
%dir %{py_sitedir}/%{module}/commands
%{py_sitedir}/%{module}/commands/*.py[co]
%dir %{py_sitedir}/%{module}/interfaces
%{py_sitedir}/%{module}/interfaces/*.py[co]
%dir %{py_sitedir}/%{module}/interfaces/images
%{py_sitedir}/%{module}/interfaces/images/*.py[co]
%{py_sitedir}/%{module}/interfaces/images/folder.png
%{py_sitedir}/%{module}/interfaces/images/package-available-locked.png
%{py_sitedir}/%{module}/interfaces/images/package-available.png
%{py_sitedir}/%{module}/interfaces/images/package-broken.png
%{py_sitedir}/%{module}/interfaces/images/package-downgrade.png
%{py_sitedir}/%{module}/interfaces/images/package-install.png
%{py_sitedir}/%{module}/interfaces/images/package-installed-locked.png
%{py_sitedir}/%{module}/interfaces/images/package-installed-outdated.png
%{py_sitedir}/%{module}/interfaces/images/package-installed.png
%{py_sitedir}/%{module}/interfaces/images/package-new-locked.png
%{py_sitedir}/%{module}/interfaces/images/package-new.png
%{py_sitedir}/%{module}/interfaces/images/package-purge.png
%{py_sitedir}/%{module}/interfaces/images/package-reinstall.png
%{py_sitedir}/%{module}/interfaces/images/package-remove.png
%{py_sitedir}/%{module}/interfaces/images/package-upgrade.png
%{py_sitedir}/%{module}/interfaces/images/smart.png
%dir %{py_sitedir}/%{module}/interfaces/text
%{py_sitedir}/%{module}/interfaces/text/*.py[co]
%dir %{py_sitedir}/%{module}/plugins
%{py_sitedir}/%{module}/plugins/*.py[co]
%dir %{py_sitedir}/%{module}/util
%{py_sitedir}/%{module}/util/*.py[co]

%files update
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/smart-update

%files gui
%defattr(644,root,root,755)
%dir %{py_sitedir}/%{module}/interfaces/gtk
%{py_sitedir}/%{module}/interfaces/gtk/*.py[co]
%{_desktopdir}/smart.desktop
%{_pixmapsdir}/smart.png

%files -n ksmarttray
%defattr(644,root,root,755)
%attr(775,root,root) %{_bindir}/ksmarttray
%{_datadir}/apps/ksmarttray
