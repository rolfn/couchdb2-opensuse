# Copyright 2016 Adrien Vergé
# adapted for openSUSE: Rolf Niepraschk <Rolf.Niepraschk@gmx.de>
#
# see: https://github.com/adrienverge/copr-couchdb
#

%define couchdb_user couchdb
%define couchdb_group couchdb
%define couchdb_home %{_localstatedir}/lib/%{name}

Name:          couchdb
Version:       2.0.0
Release:       3.1
Summary:       A document database server, accessible via a RESTful JSON API
Group:         Applications/Databases
License:       Apache
URL:           http://couchdb.apache.org/
Source0:       http://www.apache.org/dist/%{name}/source/%{version}/apache-couchdb-%{version}.tar.gz
Source1:       %{name}.service
Source2:       usr-bin-couchdb
Patch1:        0001-Trigger-cookie-renewal-on-_session.patch
Patch2:        0002-Read-config-from-env-COUCHDB_VM_ARGS-and-COUCHDB_INI.patch

BuildRequires: erlang
BuildRequires: erlang-asn1
BuildRequires: erlang-devel
BuildRequires: erlang-rebar
BuildRequires: erlang-otp
BuildRequires: erlang-otp-devel
BuildRequires: erlang-os_mon
BuildRequires: erlang-xmerl
BuildRequires: erlang-eunit
BuildRequires: erlang-public_key 
BuildRequires: erlang-reltool

BuildRequires: epmd
BuildRequires: js-devel
BuildRequires: libicu-devel

Requires:       erlang

Requires(pre): shadow
Requires(post): systemd
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
%patch1 -p1 -b .cookie-renewal
%patch2 -p1 -b .config-from-env


%build
./configure --skip-deps --disable-docs

make release %{?_smp_mflags}

# Store databases in /var/lib/couchdb
sed -i 's|\./data\b|%{couchdb_home}|g' rel/couchdb/etc/default.ini

%install
mkdir -p %{buildroot}/opt
cp -r rel/couchdb %{buildroot}/opt

install -D -m 755 %{SOURCE2} %{buildroot}%{_bindir}/%{name}

# Have conf in /etc/couchdb, not /opt/couchdb/etc
mkdir -p %{buildroot}%{_sysconfdir}
mv %{buildroot}/opt/couchdb/etc %{buildroot}%{_sysconfdir}/%{name}
mkdir %{buildroot}%{_sysconfdir}/%{name}/local.d
mkdir %{buildroot}%{_sysconfdir}/%{name}/default.d

install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

mkdir -p %{buildroot}/%{couchdb_home}

rmdir %{buildroot}/opt/couchdb/var/log %{buildroot}/opt/couchdb/var


%pre
getent group %{couchdb_group} >/dev/null || groupadd -r %{couchdb_group}
getent passwd %{couchdb_user} >/dev/null || \
  useradd -r -g %{couchdb_group} -d %{couchdb_home} -s /sbin/nologin %{couchdb_user}

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
%config %attr(0644, %{name}, %{name}) %{_sysconfdir}/%{name}/default.ini
%config(noreplace) %attr(0644, %{name}, %{name}) %{_sysconfdir}/%{name}/local.ini
%config(noreplace) %attr(0644, %{name}, %{name}) %{_sysconfdir}/%{name}/vm.args

%dir %attr(0755, %{couchdb_user}, %{couchdb_group}) %{couchdb_home}

%{_unitdir}/%{name}.service

%changelog
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
