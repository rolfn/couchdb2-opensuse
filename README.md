# couchdb2-opensuse
Ingredients for openSUSE CouchDB 2.x packages adapted from 
[this repository](https://github.com/adrienverge/copr-couchdb). 
The couchdb source code: http://www.apache.org/dist/couchdb/source/

### Required packages for the build process

```
sudo zypper install erlang erlang-rebar erlang-reltool erlang-epmd \
  libicu-devel pkg-config autoconf213 mozilla-nspr-devel rpmbuild \
  libffi-devel
sudo zypper install -t pattern devel_C_C++
```

### Creation of rpm packages (src and bin)

Do the following calls as a normal user (not as root).

```
mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
```

#### couch-js / couch-js-devel

```
./build-couch-js
```

#### couchdb

```
sudo zypper install ~/rpmbuild/RPMS/x86_64/couch-js-devel-1.8.5-21.x86_64.rpm

./build-couchdb 2.3.0 # adapt the version
```


For the results look at:

```
~/rpmbuild/RPMS/x86_64/
~/rpmbuild/SRPMS/
```

Tested with »Tumbleweed«, »Leap 15.0«, and »Leap 42.3«.
   
### Install 
```
sudo zypper rm libmozjs185-1_0 # if installed
sudo zypper install ~/rpmbuild/RPMS/x86_64/couch-js-1.8.5-21.x86_64.rpm \
  ~/rpmbuild/RPMS/x86_64/couchdb-2.3.0-1.x86_64.rpm # adapt the version
```

### Enable Service and Start
```
sudo systemctl enable couchdb.service
sudo systemctl daemon-reload
sudo systemctl start couchdb.service
sudo systemctl status couchdb.service
```

Edit `/etc/couchdb/local.ini` maybe necessary before starting the database.
 
