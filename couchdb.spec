# Copyright 2016 Adrien Vergé
# adapted for openSUSE: Rolf Niepraschk <Rolf.Niepraschk@gmx.de>, 2019
#
# see: https://github.com/adrienverge/copr-couchdb
#

%define couchdb_user couchdb
%define couchdb_group couchdb
%define couchdb_data %{_localstatedir}/lib/%{name}
%define couchdb_home /opt/%{name}

Name:          couchdb
Version:       2.3.1
Release:       3
Summary:       A document database server, accessible via a RESTful JSON API
Group:         Applications/Databases
License:       Apache
URL:           http://couchdb.apache.org/
Source0:  http://apache.mirrors.ovh.net/ftp.apache.org/dist/couchdb/source/%{version}/apache-couchdb-%{version}.tar.gz
Source1:       %{name}.service
Source2:       usr-bin-couchdb
Patch1:        0002-Read-config-from-env-COUCHDB_VM_ARGS-and-COUCHDB_INI.patch

BuildRequires: erlang
BuildRequires: erlang-rebar
BuildRequires: erlang-reltool
BuildRequires: erlang-epmd
BuildRequires: gcc-c++
BuildRequires: couch-js-devel
BuildRequires: libicu-devel 
BuildRequires: pkg-config
BuildRequires: python3

Requires:       erlang
Requires:       couch-js

Requires(pre): shadow
Requires(post): systemd
Requires(post): python3-progressbar
Requires(post): python3-requests
Requires(preun): systemd

%description
Apache CouchDB is a distributed, fault-tolerant and schema-free
document-oriented database accessible via a RESTful HTTP/JSON API.
Among other features, it provides robust, incremental replication
with bi-directional conflict detection and resolution, and is
queryable and indexable using a table-oriented view engine with
JavaScript acting as the default view definition language.


%prep
%setup -q -n apache-couchdb-%{version}
%patch1 -p1 -b .config-from-env

%build
./configure --skip-deps --disable-docs

make release %{?_smp_mflags}

# Store databases in /var/lib/couchdb
sed -i 's|\./data\b|%{couchdb_data}|g' rel/couchdb/etc/default.ini

%install
mkdir -p %{buildroot}/opt
cp -r rel/couchdb %{buildroot}/opt

install -D -m 755 %{SOURCE2} %{buildroot}%{_bindir}/%{name}

# Have conf in /etc/couchdb, not /opt/couchdb/etc
mkdir -p %{buildroot}%{_sysconfdir}
mv %{buildroot}/opt/couchdb/etc %{buildroot}%{_sysconfdir}/%{name}

install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

mkdir -p %{buildroot}%{couchdb_data}

rmdir %{buildroot}/opt/couchdb/var/log %{buildroot}/opt/couchdb/var

%{__ln_s} -f -T /var/lib/%{name} %{buildroot}/opt/%{name}/data
%{__ln_s} -f -T /etc/%{name}     %{buildroot}/opt/%{name}/etc

%pre
getent group %{couchdb_group} >/dev/null || groupadd -r %{couchdb_group}
getent passwd %{couchdb_user} >/dev/null || \
  useradd -r -g %{couchdb_group} -d %{couchdb_home} \
  -s /sbin/nologin %{couchdb_user}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
/opt/couchdb
%{_bindir}/%{name}

%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/local.d
%dir %{_sysconfdir}/%{name}/default.d
%config %attr(0644, %{name}, %{name}) %{_sysconfdir}/%{name}/default.d/README
%config %attr(0644, %{name}, %{name}) %{_sysconfdir}/%{name}/default.ini
%config %attr(0644, %{name}, %{name}) %{_sysconfdir}/%{name}/local.d/README
%config(noreplace) %attr(0644, %{name}, %{name}) %{_sysconfdir}/%{name}/local.ini
%config(noreplace) %attr(0644, %{name}, %{name}) %{_sysconfdir}/%{name}/vm.args

%dir %attr(0755, %{couchdb_user}, %{couchdb_group}) %{couchdb_data} 

%{_unitdir}/%{name}.service

%changelog
* Mon Dec 17 2018 Rolf Niepraschk <Rolf.Niepraschk@gmx.de>
- Update to new upstream version (skip 2.2 that has bugs)
- Customizing args file is now supported upstream

* Mon Aug 06 2018 Rolf Niepraschk <Rolf.Niepraschk@gmx.de>
- Test with 2.2.0-RC3
- Replace js-devel by couch-js-devel

* Fri Aug 03 2018 Rolf Niepraschk <Rolf.Niepraschk@gmx.de>
- Update to version 2.2.0-RC2
- Replace package "libmozjs185" by the self created package "couch-js"

* Thu Aug 02 2018 Rolf Niepraschk <Rolf.Niepraschk@gmx.de>
- Update to new upstream version
- Increase number of open file descriptors

* Sun Dec 24 2017 Rolf Niepraschk <Rolf.Niepraschk@gmx.de> 2.1.1-1
- Update to version 2.1.1

* Thu Aug 10 2017 Rolf Niepraschk <Rolf.Niepraschk@gmx.de> 2.1.0-1
- Update to version 2.1.0

* Tue Nov 15 2016 Rolf Niepraschk <Rolf.Niepraschk@gmx.de> 2.0.0-3.1
- Adapted for openSUSE(systemd based)

* Mon Sep 26 2016 Adrien Vergé <adrienverge@gmail.com> 2.0.0-3
- Forward signals received by launcher script

* Sat Sep 24 2016 Adrien Vergé <adrienverge@gmail.com> 2.0.0-2
- Provide a launcher script in /usr/bin

* Sat Sep 24 2016 Adrien Vergé <adrienverge@gmail.com> 2.0.0-1
- Update to stable version 2.0.0
- Update patch to take config files from environment
- Remove unneeded systemd BuildRequires

* Fri Sep 9 2016 Adrien Vergé <adrienverge@gmail.com> 2.0.0RC4-8
- Add patch to take config files from environment

* Thu Sep 8 2016 Adrien Vergé <adrienverge@gmail.com> 2.0.0RC4-7
- Store data in /var/lib/couchdb instead of /opt/couchdb/data
- Remove unneeded BuildRequires
- Remove unused /opt/couchdb/var/log dir

* Fri Sep 2 2016 Adrien Vergé <adrienverge@gmail.com> 2.0.0RC4-6
- Patch https://github.com/apache/couchdb-couch/pull/194/commits/9970f18

* Thu Sep 1 2016 Adrien Vergé <adrienverge@gmail.com> 2.0.0RC4-5
- Restore `--disable-docs` because they take 12 MiB

* Thu Sep 1 2016 Adrien Vergé <adrienverge@gmail.com> 2.0.0RC4-4
- Don't install `npm` because Fauxton is already built
- Remove `--disable-docs` because they are already built

* Thu Sep 1 2016 Adrien Vergé <adrienverge@gmail.com> 2.0.0RC4-3
- Use dist version from Apache instead of git sources
- Remove unneeded Requires
- Remove unneeded BuildRequires `help2man`

* Wed Aug 31 2016 Adrien Vergé <adrienverge@gmail.com> 2.0.0RC4-2
- Put conf files in /etc/couchdb instead of /opt/couchdb/etc

* Wed Aug 31 2016 Adrien Vergé <adrienverge@gmail.com> 2.0.0RC4-1
- Initial RPM release
