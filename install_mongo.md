# Installation

```
sudo zypper addrepo --gpgcheck "https://repo.mongodb.org/zypper/suse/15/mongodb-org/6.0/x86_64/" mongodb
sudo rpm --import https://www.mongodb.org/static/pgp/server-6.0.asc
sudo zypper ref
sudo zypper -n install mongodb-org
sudo systemctl start mongod.service
```

## Useful operations

Call `mongosh` from the localhost to launch the interactive mongo interface and connect to the DB.

Queries looks like

```
classDB> db.bugzilla.find()
[
  {
    _id: ObjectId("641f2a89b4da3e62771d6f59"),
    Name: 'ABC',
    Class: '5',
    Roll_No: '12',
    Age: '11'
  }
]
```

Note that classDB is the name of the DB and bugzilla is the document which have created.
