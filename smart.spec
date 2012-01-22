# TODO
# - bundled and modified software:
#  - pexpect-0.999 http://pexpect.sourceforge.net/
#
# Conditional build:
%bcond_with	ksmarttray	# build ksmarttray (KDE3)

%define	module smart
Summary:	Next generation package handling tool
Summary(pl.UTF-8):	Narzędzie do obsługi pakietów nowej generacji
Name:		smart
Version:	1.4.1
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://launchpad.net/smart/trunk/%{version}/+download/%{name}-%{version}.tar.bz2
# Source0-md5:	573ef32ba177a6b3c4bf7ef04873fcb6
Source1:	%{name}-distro.py
Source2:	%{name}.desktop
Source3:	%{name}-kde.desktop
Source4:	th.channel
Source5:	th-archive.channel
Source6:	th-multilib.channel
Source7:	th-obsolete.channel
Source8:	th-ready.channel
Source9:	th-test.channel
Patch0:		%{name}-syslibs.patch
Patch1:		%{name}-pyc.patch
Patch4:		%{name}-missingok.patch
Patch5:		%{name}-pycurl-segfaults.patch
URL:		http://labix.org/smart/
BuildRequires:	gettext-devel
%{?with_kde:BuildRequires:	kdelibs-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
Requires:	python-cElementTree
Requires:	python-elementtree
Requires:	python-rpm
%pyrequires_eq  python-modules
Suggests:	gksu
Suggests:	smart-config
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Smart Package Manager is a next generation package handling tool.

%description -l pl.UTF-8
Smart Package Manager to narzędzie do obsługi pakietów nowej
generacji.

%package update
Summary:	Allows execution of 'smart update' by normal users (suid)
Summary(pl.UTF-8):	Pakiet (suid) pozwalający wykonywać "smart update" zwykłym użytkownikom
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description update
Allows execution of 'smart update' by normal users through a special
suid command.

%description update -l pl.UTF-8
Ten pakiet pozwala wykonywać "smart update" zwykłym użytkownikom
poprzez specjalne polecenie suid.

%package gui
Summary:	Graphical user interface for the Smart Package Manager
Summary(pl.UTF-8):	Graficzny interfejs użytkownika do zarządcy pakietów Smart
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	gksu
Requires:	python-pygtk-gtk

%description gui
Graphical user interface for the Smart Package Manager.

%description gui -l pl.UTF-8
Graficzny interfejs użytkownika do zarządcy pakietów Smart.

%package -n ksmarttray
Summary:	KDE tray program for watching updates with Smart Package Manager
Summary(pl.UTF-8):	Program zasobnika KDE do oglądania uaktualnień przy użyciu zarządcy pakietów Smart
Group:		Applications/System
Requires:	smart-update = %{version}-%{release}

%description -n ksmarttray
KDE tray program for watching updates with Smart Package Manager.

%description -n ksmarttray -l pl.UTF-8
Program zasobnika KDE do oglądania uaktualnień przy użyciu zarządcy
pakietów Smart.

%description -n ksmarttray -l pt.UTF-8
Programa tray do KDE para verificar atualizações com o Smart Package
Manager.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch4 -p1
#%patch5 -p0

# %{_libdir} is hardcoded
%{__sed} -i -e's,/usr/lib/,%{_libdir}/,' smart/const.py

rm -r smart/util/elementtree
rm -r smart/util/celementtree
rm smart/util/optparse.py

%build
# CC/CFLAGS is only for arch packages - remove on noarch packages
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build

# smart-update
%{__make} -C contrib/smart-update \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%if %{with ksmarttray}
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
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_libdir}/smart} \
	$RPM_BUILD_ROOT/var/lib/smart/{channels,packages} \
	$RPM_BUILD_ROOT/etc/smart/channels

%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

cp -f contrib/smart-update/smart-update $RPM_BUILD_ROOT%{_bindir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}/%{name}-kde.desktop
install -p smart/interfaces/images/smart.png $RPM_BUILD_ROOT%{_pixmapsdir}/smart.png
# Currently needs to hardcode %{_libdir}, as this is hardcoded in the
# code, too.
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_libdir}/smart/distro.py

%if %{with ksmarttray}
%{__make} -C contrib/ksmarttray install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%define	_pld_multilib_conf %{nil}
%ifarch i486 i686 ppc sparc alpha athlon
	%define		_ftp_arch	%{_target_cpu}
%endif
%ifarch %{x8664}
	%define		_ftp_arch	x86_64
	%define		_pld_multilib_conf %{SOURCE6}
%endif
%ifarch i586
	%define		_ftp_arch	i486
%endif
%ifarch pentium2 pentium3 pentium4
	%define		_ftp_arch	i686
%endif

for f in %{SOURCE4} %{SOURCE5} %{SOURCE7} %{SOURCE8} %{SOURCE9} %{_pld_multilib_conf}; do
	ff=$(basename $f)
	%{__sed} -e 's|%%ARCH%%|%{_ftp_arch}|g' $f >$RPM_BUILD_ROOT/etc/smart/channels/$ff
done

mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{es_ES,es}

touch $RPM_BUILD_ROOT/var/lib/smart/packages/{cache,config}

%find_lang %{name}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc HACKING README LICENSE TODO IDEAS
%dir /etc/smart/channels
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/smart/channels/th*.channel
%attr(755,root,root) %{_bindir}/smart
%{_mandir}/man8/smart.8*
%{_libdir}/smart
%dir /var/lib/smart
%dir /var/lib/smart/channels
%dir /var/lib/smart/packages
%ghost /var/lib/smart/packages/cache
%ghost /var/lib/smart/packages/config

%attr(755,root,root) %{py_sitedir}/%{module}/ccache.so
%attr(755,root,root) %{py_sitedir}/%{module}/util/cdistance.so
%attr(755,root,root) %{py_sitedir}/%{module}/util/ctagfile.so
%attr(755,root,root) %{py_sitedir}/%{module}/backends/deb/_base.so
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
%{py_sitedir}/%{module}/interfaces/images/*.png
%dir %{py_sitedir}/%{module}/interfaces/text
%{py_sitedir}/%{module}/interfaces/text/*.py[co]
%dir %{py_sitedir}/%{module}/plugins
%{py_sitedir}/%{module}/plugins/*.py[co]
%dir %{py_sitedir}/%{module}/util
%{py_sitedir}/%{module}/util/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitedir}/smart-%{version}-*.egg-info
%endif

%files update
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/smart-update

%files gui
%defattr(644,root,root,755)
%dir %{py_sitedir}/%{module}/interfaces/gtk
%{py_sitedir}/%{module}/interfaces/gtk/*.py[co]
%dir %{py_sitedir}/%{module}/interfaces/qt
%{py_sitedir}/%{module}/interfaces/qt/*.py[co]
%dir %{py_sitedir}/%{module}/interfaces/qt4
%{py_sitedir}/%{module}/interfaces/qt4/*.py[co]
%{_desktopdir}/smart.desktop
%{_desktopdir}/smart-kde.desktop
%{_pixmapsdir}/smart.png

%dir %{py_sitedir}/%{module}/backends/arch
%{py_sitedir}/%{module}/backends/arch/*.py[co]

%if %{with kde}
%files -n ksmarttray
%defattr(644,root,root,755)
%attr(775,root,root) %{_bindir}/ksmarttray
%{_datadir}/apps/ksmarttray
%endif
