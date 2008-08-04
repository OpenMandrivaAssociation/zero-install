%define vname %{name}-%{version}
%define LAZYFS_VERSION 0d1d26

%define _sysconfdir /etc

Name:           zero-install
Version:        0.1.27
Release:        %mkrel 10
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

