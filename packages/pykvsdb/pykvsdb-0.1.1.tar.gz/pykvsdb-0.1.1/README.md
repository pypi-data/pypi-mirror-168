# PYKVSDB
A key-value store database written from the ground-up with speed in mind.

## Installation
PYKVSDB can be installed via pip:

```pip install pykvsdb```

## Syntax
### Setting Values
You can store a key-value pair in PYKVSDB with the ```set``` function:

```pykvsdb.set("language", "python")```
### Getting Values
To retrieve a value, use the ```get``` function:

```pykvsdb.get("language")```

### Saving to the file system
If you would like to be able to access your data later you will need to save it to the file system with ```save```:

```pykvsdb.save("test.db")```

### Loading a saved database
If you need to access a database saved to the file system again, you need to load it with ```load```:

```pykvsdb.load("test.db")```
