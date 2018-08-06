# couchdb2-opensuse
Ingredients for openSUSE CouchDB 2.x packages adapted from 
[this repository](https://github.com/adrienverge/copr-couchdb). 
The couchdb source code: http://www.apache.org/dist/couchdb/source/

### Required packages for the build process

```
sudo zypper in erlang erlang-src erlang-rebar erlang-reltool erlang-epmd \
  js-devel libicu-devel pkg-config autoconf213 mozilla-nspr-devel rpmbuild 
sudo zypper in -t pattern devel_C_C++ 
```

### Create rpm packages (src and bin)

```
mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
```

#### couch-js

```
./build-couch-js
```

#### couchdb

```
cp couchdb.service *.patch apache-couchdb-2.x.y.tar.gz usr-bin-couchdb \
  ~/rpmbuild/SOURCES/
rpmbuild -ba couchdb.spec.2.x.y 
```

For the results look at:

```
~/rpmbuild/RPMS/x86_64/
~/rpmbuild/SRPMS/
```

Tested with »Tumbleweed«, »Leap 42.1«, »Leap 42.2«, and »Leap 42.3«.
   
### Install 
```
sudo zypper install ~/rpmbuild/RPMS/x86_64/couch-js-devel-1.8.5-21.x86_64.rpm
# ^--- (only for rebuild the couchdb bin rpm)
sudo zypper install ~/rpmbuild/RPMS/x86_64/couch-js-1.8.5-21.x86_64.rpm \
  ~/rpmbuild/RPMS/x86_64/couchdb-2.x.y*.x86_64.rpm
```

### Enable Service and Start
```
sudo systemctl enable couchdb.service
sudo systemctl daemon-reload
sudo systemctl start couchdb.service
```

Edit `/etc/couchdb/local.ini` maybe necessary before starting the process.
 
