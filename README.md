# couchdb2-opensuse
Ingredients for openSUSE CouchDB 2.x packages adapted from 
[this repository](https://github.com/adrienverge/copr-couchdb). 
The couchdb source code: http://www.apache.org/dist/couchdb/source/

### Required packages for the build process

* erlang
* erlang-src
* erlang-rebar
* erlang-reltool
* erlang-epmd
* js-devel
* libicu-devel 
* pkg-config


### Create rpm packages (src and bin)
```
cp couchdb.service *.patch apache-couchdb-2.x.y.tar.gz ~/rpmbuild/SOURCES
rpmbuild -ba couchdb.spec.2.x.y 
```

Tested with »Tumbleweed«, »Leap 42.1«, and »Leap 42.2«.
   
### Install 
```
sudo zypper install ~/rpmbuild/RPMS/x86_64/couchdb-2.x.y*.x86_64.rpm
```

### Enable Service and Start
```
sudo systemctl enable couchdb.service
sudo systemctl start couchdb.service
```

Edit `/etc/couchdb/local.ini` maybe necessary before starting the process.
 
