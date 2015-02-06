%define name syncany

Name:		%{name}
Version:	0.1.alpha
Release:	4
License:	GPLv3
Summary:	Syncany is an open-source file synchronization and filesharing application
Group:		Archiving/Backup
URL:		https://launchpad.net/syncany/
# $ bzr branch lp:synany
# $ bzr export --root="syncany-0.1.alpha/" ~/BuildSystem/syncany/SOURCES/syncany-0.1.alpha.tar.bz2
Source0:	%{name}-%{version}.tar.bz2
# From https://launchpad.net/~mariodebian/+archive/syncany
Source1:	syncany
Source2:	syncany-autostart
Source3:	syncany.desktop
Source4:	syncany-autostart.desktop
Suggests:	%{name}-doc
# BuildRequires for Syncany Java part
BuildRequires:	ant
BuildRequires:	ant-apache-regexp
BuildRequires:	ant-nodeps
BuildRequires:	java-devel
# BuildRequires for Syncany Nautilus extension
BuildRequires:	gtk2-devel
BuildRequires:	atk-devel
BuildRequires:	cairo-devel
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	pango-devel
BuildRequires:	glib2-devel
BuildRequires:	pixman-devel
BuildRequires:	freetype2-devel
BuildRequires:	png-devel
BuildRequires:	nautilus-devel

%description
Syncany is an open-source file synchronization and filesharing
application. It allows users to backup and share certain folders of
their workstations using any kind of storage, e.g. FTP, Amazon S3 or
Google Storage.

While the basic idea is similar to Dropbox and JungleDisk, Syncany is
open-source and additionally provides data encryption and more
flexibility in terms of storage type and provider:

- Data encryption: Syncany encrypts the files locally, so that any
  online storage can be used even for sensitive data.

- Arbitrary storage: Syncany uses a plug-in based storage system. It can
  be used with any type of remote storage.

%files
%{_datadir}/%{name}/
%{_datadir}/pixmaps/%{name}.png

%package doc
Summary:	Syncany Documentation
BuildArch:	noarch

%description doc
Documentation for Syncany

%files doc
%doc %{_docdir}/%{name}-doc/

%package nautilus
Summary:	Syncany Nautilus extension

%description nautilus
Synany extension for Nautilus file browser.

%files nautilus
%{_libdir}/nautilus/

%prep
%setup -q -n %{name}-%{version}
%apply_patches

%ifarch x86_64
pushd nautilus-syncany
for f in nbproject/{configurations.xml,Makefile-Debug.mk}; do
sed -ri \
	-e 's|/usr/lib/gtk-2.0/include|/usr/lib64/gtk-2.0/include|g' \
	-e 's|/usr/lib/glib-2.0/include|/usr/lib64/glib-2.0/include|g' \
	$f
done;
popd
%endif

%build

# Building Syncany
pushd syncany
ant linux
popd

# Building Nautilus extension
pushd nautilus-syncany
%make CONF=Debug
popd

%install

# Installing Syncany
pushd syncany/dist
for f in $(find {bin,conf,lib,res} -type f); do
	%{__install} -D $f %{buildroot}%{_datadir}/%{name}/$f
done;
for f in README LICENSE; do
	%{__install} -D $f %{buildroot}%{_docdir}/%{name}-doc/$f
done;
popd

%{__install} -d %{buildroot}%{_datadir}/pixmaps/
pushd %{buildroot}
ln -s ./%{_datadir}/%{name}/res/logo64.png ./%{_datadir}/pixmaps/%{name}.png
popd

# Installing Nautilus extension
pushd nautilus-syncany
	%{__install} -m0755 -D dist/*/GNU-Linux-*/libnautilus-syncany.so %{buildroot}%{_libdir}/nautilus/extensions-2.0/libnautilus-syncany.so
popd
