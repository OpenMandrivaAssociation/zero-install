%define vname %{name}-%{version}
%define LAZYFS_VERSION 0d1d26

%define _sysconfdir /etc

Name:           zero-install
Version:        0.1.27
Release:        %mkrel 11
Summary:        Removes the need to install software

Group:          System/Servers
License:        GPLv2+
URL:            http://0install.net/
Source0:        http://heanet.dl.sourceforge.net/sourceforge/zero-install/%{vname}.tar.gz.gpg
Patch0:         zero-install-0.1.26-build.patch.bz2
Patch1:         zero-install-0.1.26-initscript.patch.bz2
Patch2:         zero-install-0.1.26-noload.patch.bz2
# (fc) 0.1.27-4mdk fix build with latest dbus
Patch3:         zero-install-0.1.27-dbus050.patch.bz2
# (nl) 0.1.27-6mdv2007.0 fix build with dbus 0.91
Patch4:         zero-install-0.1.27-build-DBUS.patch
BuildRoot:      %{_tmppath}/%{vname}-%{release}-root
BuildRequires:  dbus-devel >= 0.20
BuildRequires:  gnupg
BuildRequires:  expat-devel
Requires(pre):  rpm-helper
Requires(post): rpm-helper
Requires(preun):rpm-helper
Requires(postun):rpm-helper
Requires:       gnupg 
Requires:       wget 
Requires:       bzip2 
Requires:       tar 
Requires:       gzip
Requires:       lazyfs = %{LAZYFS_VERSION}

%description
The Zero Install system removes the need to install software or libraries by
running all programs from a network filesystem. The filesystem in question is
the Internet as a whole, with an aggressive caching system to make it as fast
as (or faster than) traditional systems such as urpmi repositories, and to
allow for offline use. It doesn't require any central authority to maintain it,
and allows users to run software without needing a root password.

# -----------------------------------------------------------------------------

%prep
# We have to unpack manually because of using GPG
%setup -c -T
cd ..
gpg -o %{vname}.tar.gz %{SOURCE0} || echo Ignoring GPG error
tar --no-same-owner -xzf %{vname}.tar.gz
rm %{vname}.tar.gz
cd %name-%version
%patch0 -p1 -b .build
%patch1 -p1 -b .initscript
%patch2 -p1 -b .noload
%patch3 -p1 -b .dbus
%patch4 -p1 -b .dbus_091

# -----------------------------------------------------------------------------

%build
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/rc.d/init.d/
%configure2_5x --with-user=zeroinst --with-distcheck=yes --prefix=/ \
               --with-initdir=%{_sysconfdir}/rc.d/init.d/
%make

# -----------------------------------------------------------------------------

%install
rm -rf "$RPM_BUILD_ROOT"
mkdir "$RPM_BUILD_ROOT"
DESTDIR="$RPM_BUILD_ROOT" make install
mkdir -p "$RPM_BUILD_ROOT"/var/cache/zero-inst
mv $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/0install $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/zero-install

# -----------------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT

# -----------------------------------------------------------------------------

%pre
# Add the "zeroinst" user
%_pre_useradd zeroinst /var/cache/zero-inst /sbin/nologin

%post
%_post_service zero-install

%preun
%_preun_service zero-install

%postun
%_postun_userdel zeroinst

# -----------------------------------------------------------------------------

%files
%defattr(-,root,root,-)
/bin/0run
/usr/bin/0refresh
/usr/sbin/zero-install
%{_sysconfdir}/rc.d/init.d/zero-install
%attr(755, zeroinst, root) %dir /var/cache/zero-inst
%doc NEWS README

# -----------------------------------------------------------------------------



%changelog
* Wed Sep 09 2009 Thierry Vignaud <tvignaud@mandriva.com> 0.1.27-11mdv2010.0
+ Revision: 435379
- rebuild

* Mon Aug 04 2008 Thierry Vignaud <tvignaud@mandriva.com> 0.1.27-10mdv2009.0
+ Revision: 263030
- rebuild
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Dec 27 2007 Adam Williamson <awilliamson@mandriva.org> 0.1.27-7mdv2008.1
+ Revision: 138682
- rebuild for new expat
- new license policy

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request
    - import zero-install


* Sat Sep 02 2006 Nicolas Lécureuil <neoclust@mandriva.org> 0.1.27-6mdv2007.0
- Rebuild against new DBUS
        Add patch 4: Fix build  with D-Bus 0.91
- Fix some rpmlint warnings
 
* Fri Jan 27 2006 Frederic Crozat <fcrozat@mandriva.com> 0.1.27-5mdk
- Rebuild with latest dbus

* Thu Nov 03 2005 Frederic Crozat <fcrozat@mandriva.com> 0.1.27-4mdk
- Patch3: fix build with latest dbus

* Wed Sep 28 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.1.27-3mdk
- Fix BuildRequires ( again )

* Wed Sep 28 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.1.27-2mdk
- Fix BuildRequires
- mkrel 
- Fix PreReq

* Mon Apr  4 2005 Frederic Lepied <flepied@mandrakesoft.com> 0.1.27-1mdk
- New version

* Thu Jan 20 2005 Emmanuel Blindauer <mdk@agat.net> 0.1.26-4mdk
- update the require to the latest lazyfs

* Wed Sep  1 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.1.26-3mdk
- fixed summary
- added a require on the right version of lazyfs
- reworked init script: o mount and unmount the filesystem
                        o use standard functions
                        o provide a status sub-command

* Wed Sep  1 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.1.26-2mdk
- Requires lazyfs

* Tue Aug 31 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.1.26-1mdk
- new version

* Sat Jun 19 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.1.24-1mdk
- initial packaging

* Sat Jun 5 2004 Alastair Porter
- Update to 0.1.23

* Fri Apr 24 2004 Thomas Leonard <tal197[AT]users.sf.net> - 0.1.22-1
- Initial RPM release.
