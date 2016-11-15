# couchdb2-opensuse
Ingredients for openSUSE CouchDB 2.0 packages adapted from 
[this repository](https://github.com/adrienverge/copr-couchdb). 
The couchdb source code: http://www.apache.org/dist/couchdb/source/

### Required packages for the build process

* erlang
* erlang-asn1
* erlang-devel
* erlang-rebar
* erlang-otp
* erlang-otp-devel
* erlang-os_mon
* erlang-xmerl
* erlang-eunit
* erlang-public_key 
* erlang-reltool
* js-devel
* libicu-devel


### Create rpm packages (src and bin)
```
cp couchdb.service *.patch apache-couchdb-2.0.0.tar.gz ~/rpmbuild/SOURCES
rpmbuild -ba couchdb.spec 
```

Tested with »openSUSE Tumbleweed«.
   
### Install 
```
sudo zypper install ~/rpmbuild/RPMS/x86_64/couchdb-2.0.0*.x86_64.rpm
```

### Enable Service and Start
```
sudo systemctl enable couchdb.service
sudo systemctl start couchdb.service
```

Edit `/etc/couchdb/local.ini` maybe necessary before starting the process.
 
