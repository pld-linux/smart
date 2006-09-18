# TODO
# - bundled and modified software:
#  - pexpect-0.999 http://pexpect.sourceforge.net/
%bcond_without	kde # not needed for GNOME
%define	module smart
Summary:	Next generation package handling tool
Summary(pl):	Narzêdzie do obs³ugi pakietów nowej generacji
Name:		smart
Version:	0.42
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://labix.org/download/smart/%{name}-%{version}.tar.bz2
# Source0-md5:	e60b411ad41dbe2e6fc57a04d82f91cb
Source1:	%{name}-distro.py
Source2:	%{name}.desktop
Source3:	%{name}-kde.desktop
Patch0:		%{name}-syslibs.patch
Patch1:		%{name}-autoconf-2.6.patch
URL:		http://labix.org/smart/
%if %{with kde}
BuildRequires:	kdelibs-devel
%endif
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

%description -l pl
Smart Package Manager to narzêdzie do obs³ugi pakietów nowej
generacji.

%package update
Summary:	Allows execution of 'smart update' by normal users (suid)
Summary(pl):	Pakiet (suid) pozwalaj±cy wykonywaæ "smart update" zwyk³ym u¿ytkownikom
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description update
Allows execution of 'smart update' by normal users through a special
suid command.

%description update -l pl
Ten pakiet pozwala wykonywaæ "smart update" zwyk³ym u¿ytkownikom
poprzez specjalne polecenie suid.

%package gui
Summary:	Graphical user interface for the Smart Package Manager
Summary(pl):	Graficzny interfejs u¿ytkownika do zarz±dcy pakietów Smart
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	python-pygtk-gtk

%description gui
Graphical user interface for the Smart Package Manager.

%description gui -l pl
Graficzny interfejs u¿ytkownika do zarz±dcy pakietów Smart.

%if %{with kde}
%package -n ksmarttray
Summary:	KDE tray program for watching updates with Smart Package Manager
Summary(pl):	Program zasobnika KDE do ogl±dania uaktualnieñ przy u¿yciu zarz±dcy pakietów Smart
Group:		Applications/System
Requires:	smart-update = %{version}-%{release}

%description -n ksmarttray
KDE tray program for watching updates with Smart Package Manager.

%description -n ksmarttray -l pl
Program zasobnika KDE do ogl±dania uaktualnieñ przy u¿yciu zarz±dcy
pakietów Smart.

%description -n ksmarttray -l pt
Programa tray do KDE para verificar atualizações com o Smart Package Manager.
%endif

%prep
%setup -q
%patch0 -p1
%patch1 -p0

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

%if %{with kde}
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
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_libdir}/smart,/var/lib/smart}
python setup.py install -O1 --root=$RPM_BUILD_ROOT

cp -f contrib/smart-update/smart-update $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
%if %{with kde}
install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}/%{name}-kde.desktop
%endif
install -p smart/interfaces/images/smart.png $RPM_BUILD_ROOT%{_pixmapsdir}/smart.png
# Currently needs to hardcode %{_libdir}, as this is hardcoded in the
# code, too.
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_libdir}/smart/distro.py

%if %{with kde}
%{__make} install \
	-C contrib/ksmarttray \
	DESTDR=$RPM_BUILD_ROOT
%endif

%find_lang %{name}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc HACKING README LICENSE TODO IDEAS
%attr(755,root,root) %{_bindir}/smart
%{_mandir}/man8/smart.8.gz
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
%{py_sitescriptdir}/%{module}/interfaces/images/folder.png
%{py_sitescriptdir}/%{module}/interfaces/images/package-available-locked.png
%{py_sitescriptdir}/%{module}/interfaces/images/package-available.png
%{py_sitescriptdir}/%{module}/interfaces/images/package-broken.png
%{py_sitescriptdir}/%{module}/interfaces/images/package-downgrade.png
%{py_sitescriptdir}/%{module}/interfaces/images/package-install.png
%{py_sitescriptdir}/%{module}/interfaces/images/package-installed-locked.png
%{py_sitescriptdir}/%{module}/interfaces/images/package-installed-outdated.png
%{py_sitescriptdir}/%{module}/interfaces/images/package-installed.png
%{py_sitescriptdir}/%{module}/interfaces/images/package-new-locked.png
%{py_sitescriptdir}/%{module}/interfaces/images/package-new.png
%{py_sitescriptdir}/%{module}/interfaces/images/package-purge.png
%{py_sitescriptdir}/%{module}/interfaces/images/package-reinstall.png
%{py_sitescriptdir}/%{module}/interfaces/images/package-remove.png
%{py_sitescriptdir}/%{module}/interfaces/images/package-upgrade.png
%{py_sitescriptdir}/%{module}/interfaces/images/smart.png
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
%if %{with kde}
%{_desktopdir}/smart-kde.desktop
%endif
%{_pixmapsdir}/smart.png

%if %{with kde}
%files -n ksmarttray
%defattr(644,root,root,755)
%attr(775,root,root) %{_bindir}/ksmarttray
%{_datadir}/apps/ksmarttray
%endif
