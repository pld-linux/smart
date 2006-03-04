Summary:	Next generation package handling tool
Name:		smart
Version:	0.41
Release:	0.26.1
License:	GPL
Group:		Applications/System
URL:		http://labix.org/smart/
Source0:	http://labix.org/download/smart/%{name}-%{version}.tar.bz2
# Source0-md5:	1460dfbfe7f739ac718525c71f46b5fc
Source1:	%{name}.console
Source2:	%{name}.pam
Source3:	%{name}.desktop
Source4:	distro.py
Patch0:		%{name}-0.28-mxddcl.patch
#BuildRequires:	desktop-file-utils
BuildRequires:	gcc-c++
BuildRequires:	python-devel >= 1:2.3
#Requires:	/usr/lib/python2.4/site-packages/rpm
#Requires:	python-abi = %(python -c "import sys ; print sys.version[:3]")
%pyrequires_eq  python-modules
#Requires:	rpm-python >= 4.3.3
#Requires:	usermode
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Smart Package Manager is a next generation package handling tool.

%package update
Summary:	Allows execution of 'smart update' by normal users (suid)
Group:		Applications/System
Requires:	smart = %{version}-%{release}

%description update
Allows execution of 'smart update' by normal users through a
special suid command.

%package gui
Summary:	Graphical user interface for the smart package manager
Group:		Applications/System
#Requires:	/usr/lib/python2.4/site-packages/pygtk.py
#Requires: pygtk2
Requires:	smart = %{version}-%{release}

%description gui
Graphical user interface for the smart package manager.

%prep
%setup -q
#%patch0 -p1 -b .mxddcl
# %{_libdir} is hardcoded
perl -pi -e's,%{_libdir}/,%{_libdir}/,' smart/const.py

%build
export CFLAGS="%{rpmcflags}"
python setup.py build

%{__make} -C contrib/smart-update

%install
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
python setup.py install -O1 --root=$RPM_BUILD_ROOT
#%python_burninversion

ln -sf consolehelper $RPM_BUILD_ROOT%{_bindir}/smart-root

install -d $RPM_BUILD_ROOT/etc/security/console.apps
install -d $RPM_BUILD_ROOT/etc/pam.d
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/security/console.apps/smart-root
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/smart-root

cp -f contrib/smart-update/smart-update $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_datadir}/applications
#desktop-file-install --vendor fedora                            \
#        --dir $RPM_BUILD_ROOT%{_datadir}/applications              \
#        --add-category X-Fedora                                 \

install %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/applications

install -d  $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -p smart/interfaces/images/smart.png \
    $RPM_BUILD_ROOT%{_datadir}/pixmaps/smart.png

# Currently needs to hardcode %{_libdir}, as this is hardcoded in the
# code, too.
install -d $RPM_BUILD_ROOT%{_libdir}/smart
install -p %{SOURCE4} $RPM_BUILD_ROOT%{_libdir}/smart/

%find_lang %{name}

# Create a list w/o smart/interfaces/gtk to avoid warbing of duplicate
# in the %files section (otherwise including all and %excluding works,
# too

echo "%%defattr(-,root,root,-)" > %{name}.fileslist
find $RPM_BUILD_ROOT%{py_sitedir}/smart -type d \
| grep -v %{py_sitedir}/smart/interfaces/gtk \
  | sed -e"s,$RPM_BUILD_ROOT,%%dir ," \
  >> %{name}.fileslist
find $RPM_BUILD_ROOT%{py_sitedir}/smart \! -type d \! -name \*.pyo \
| grep -v %{py_sitedir}/smart/interfaces/gtk \
  | sed -e"s,$RPM_BUILD_ROOT,," \
  >> %{name}.fileslist
find $RPM_BUILD_ROOT%{py_sitedir}/smart -name \*.pyo \
| grep -v %{py_sitedir}/smart/interfaces/gtk \
  | sed -e"s,$RPM_BUILD_ROOT,%%ghost ," \
  >> %{name}.fileslist

# %files does not take two -f arguments
cat %{name}.lang >> %{name}.fileslist

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.fileslist
%defattr(644,root,root,755)
%doc HACKING README LICENSE TODO IDEAS
%attr(755,root,root) %{_bindir}/smart
%attr(755,root,root) %{_bindir}/smart-root
%config /etc/security/console.apps/smart-root
%config /etc/pam.d/smart-root
%{_libdir}/smart

%files update
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/smart-update

%files gui
%defattr(644,root,root,755)
%dir %{py_sitedir}/smart/interfaces/gtk
%{py_sitedir}/smart/interfaces/gtk/*.py
%{py_sitedir}/smart/interfaces/gtk/*.pyc
%ghost %{py_sitedir}/smart/interfaces/gtk/*.pyo
%{_desktopdir}/smart.desktop
%{_pixmapsdir}/smart.png
